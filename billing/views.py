from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import re

from .models import MenuItem, Table, Customer, Bill


# ──────────────────────────────────────────────
#  Page views
# ──────────────────────────────────────────────

def dashboard(request):
    tables = Table.objects.all()
    # Sync table status with active bills:
    # - open bills count only when they have items
    # - pending bills are always active
    for table in tables:
        has_open_bill = Bill.objects.filter(table=table, status='open').exclude(items=[]).exists()
        has_pending_bill = Bill.objects.filter(table=table, status='pending').exists()
        if table.status == 'occupied' and not has_open_bill and not has_pending_bill:
            table.status = 'free'
            table.save()
        elif table.status == 'free' and (has_open_bill or has_pending_bill):
            table.status = 'occupied'
            table.save()

    open_bills = Bill.objects.filter(status='open').exclude(items=[]).count()
    pending_bills = Bill.objects.filter(status='pending')
    paid_bills = Bill.objects.filter(status='paid')
    total_menu = MenuItem.objects.filter(is_available=True).count()
    
    # Get list of table IDs with pending bills
    pending_table_ids = list(pending_bills.values_list('table_id', flat=True).distinct())
    
    context = {
        'tables': Table.objects.all(),
        'open_bills': open_bills,
        'pending_bills': pending_bills,
        'pending_table_ids': pending_table_ids,
        'paid_bills': paid_bills,
        'total_menu': total_menu,
    }
    return render(request, 'billing/dashboard.html', context)

def billing_view(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    # Load bill in order: pending > open > create new
    bill = Bill.objects.filter(table=table, status='pending').order_by('-updated_at').first()
    if not bill:
        bill = Bill.objects.filter(table=table, status='open').order_by('-updated_at').first()
        
    if not bill:
        bill = Bill.objects.create(table=table, status='open', customer_name='Guest')
    elif bill.status == 'pending':
        # Keep table occupied if bill is pending
        table.status = 'occupied'
        table.save()

    # Open bill without items should keep table free (white on dashboard).
    if bill.status == 'open' and not bill.items:
        table.status = 'free'
        table.save()
    
    return render(request, 'billing/billing.html', {'table': table, 'bill': bill})

# ──────────────────────────────────────────────
#  NLP: parse voice text → matched menu items
# ──────────────────────────────────────────────
WORD_TO_NUM = {
    'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,
    'six':6,'seven':7,'eight':8,'nine':9,'ten':10,
    'ek':1,'do':2,'teen':3,'char':4,'paanch':5,
}

def extract_quantity(text_before_item):
    """Extract qty from words immediately before the item name."""
    words = text_before_item.strip().split()
    for w in reversed(words[-3:]):
        if w.isdigit():
            return int(w)
        if w in WORD_TO_NUM:
            return WORD_TO_NUM[w]
    return 1


def fuzzy_match(query, menu_items):
    """Simple fuzzy match: score by how many query words appear in item name."""
    query_words = set(re.sub(r'[^a-z0-9 ]', '', query.lower()).split())
    best, best_score = None, 0
    for item in menu_items:
        name_words = set(item.item_name.lower().split())
        score = len(query_words & name_words) / max(len(name_words), 1)
        if score > best_score:
            best, best_score = item, score
    return best if best_score >= 0.4 else None


@csrf_exempt
def parse_voice(request):
    """
    POST { "text": "2 cheese pizza and 1 coke" }
    Returns list of matched items with qty.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data = json.loads(request.body)
    text = data.get('text', '').lower()
    menu_items = MenuItem.objects.filter(is_available=True)

    # Split on connectors
    segments = re.split(r'\band\b|,|aur', text)
    matched = []

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        # Pull out any number from segment
        qty = 1
        for word, num in WORD_TO_NUM.items():
            if re.search(r'\b' + word + r'\b', segment):
                qty = num
                segment = re.sub(r'\b' + word + r'\b', '', segment).strip()
                break
        num_match = re.search(r'\b(\d+)\b', segment)
        if num_match:
            qty = int(num_match.group(1))
            segment = segment.replace(num_match.group(0), '').strip()

        item = fuzzy_match(segment, menu_items)
        if item:
            matched.append({
                'item_id': item.id,
                'name': item.item_name,
                'qty': qty,
                'price': float(item.price),
                'subtotal': round(qty * float(item.price), 2),
            })

    return JsonResponse({'items': matched, 'raw_text': data.get('text', '')})


# ──────────────────────────────────────────────
#  Bill API
# ──────────────────────────────────────────────

@csrf_exempt
def add_items_to_bill(request, bill_id):
    """POST { "items": [...] }  — replaces or merges items in bill."""
    bill = get_object_or_404(Bill, id=bill_id)
    data = json.loads(request.body)
    new_items = data.get('items', [])

    # Merge: update qty if item already exists
    existing = {i['item_id']: i for i in bill.items}
    for ni in new_items:
        if ni['item_id'] in existing:
            existing[ni['item_id']]['qty'] += ni['qty']
            existing[ni['item_id']]['subtotal'] = round(
                existing[ni['item_id']]['qty'] * ni['price'], 2
            )
        else:
            existing[ni['item_id']] = ni

    bill.items = list(existing.values())
    bill.calculate_totals()
    bill.save()

    # Once at least one item exists on an open bill, table becomes occupied.
    if bill.status == 'open' and bill.items:
        table = bill.table
        table.status = 'occupied'
        table.save()

    return JsonResponse({
        'success': True,
        'items': bill.items,
        'subtotal': float(bill.subtotal),
        'gst_amount': float(bill.gst_amount),
        'total': float(bill.total),
    })


@csrf_exempt
def remove_item_from_bill(request, bill_id, item_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.items = [i for i in bill.items if i['item_id'] != item_id]
    bill.calculate_totals()
    bill.save()

    # If all items are removed from an open bill, free the table again.
    if bill.status == 'open' and not bill.items:
        table = bill.table
        table.status = 'free'
        table.save()

    return JsonResponse({'success': True, 'items': bill.items,
                         'subtotal': float(bill.subtotal),
                         'gst_amount': float(bill.gst_amount),
                         'total': float(bill.total)})


@csrf_exempt
def generate_bill(request, bill_id):
    """Mark bill as pending payment (awaiting payment method selection)."""
    bill = get_object_or_404(Bill, id=bill_id)
    if not bill.items:
        return JsonResponse({'error': 'Cannot generate bill without items'}, status=400)

    customer_name = json.loads(request.body).get('customer_name', 'Guest')
    bill.customer_name = customer_name
    bill.status = 'pending'
    bill.save()

    table = bill.table
    table.status = 'occupied'
    table.save()

    return JsonResponse({
        'success': True,
        'bill_id': bill.id,
        'customer_name': bill.customer_name,
        'items': bill.items,
        'subtotal': float(bill.subtotal),
        'gst_amount': float(bill.gst_amount),
        'total': float(bill.total),
    })


@csrf_exempt
def checkout_table(request, table_id):
    """Free the table after customer leaves."""
    table = get_object_or_404(Table, id=table_id)
    table.status = 'free'
    table.save()
    return JsonResponse({'success': True})


@csrf_exempt
def set_payment_method(request, bill_id):
    """Set payment method for a bill and process payment."""
    bill = get_object_or_404(Bill, id=bill_id)
    data = json.loads(request.body)
    payment_method = data.get('payment_method', '').lower()
    
    # Validate payment method
    valid_methods = ['cash', 'online', 'card']
    if payment_method not in valid_methods:
        return JsonResponse({'error': 'Invalid payment method'}, status=400)
    
    bill.payment_method = payment_method
    bill.status = 'paid'
    bill.save()

    table = bill.table

    # Close any extra active bills on the same table so the table can become free.
    Bill.objects.filter(table=table, status__in=['open', 'pending']).exclude(id=bill.id).update(status='cancelled')

    table.status = 'free'
    table.save()
    
    return JsonResponse({
        'success': True,
        'bill_id': bill.id,
        'customer_name': bill.customer_name,
        'payment_method': bill.payment_method,
        'status': bill.status,
        'table_status': table.status,
        'items': bill.items,
        'subtotal': float(bill.subtotal),
        'gst_amount': float(bill.gst_amount),
        'total': float(bill.total),
    })


def get_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return JsonResponse({
        'id': bill.id,
        'items': bill.items,
        'subtotal': float(bill.subtotal),
        'gst_amount': float(bill.gst_amount),
        'total': float(bill.total),
        'status': bill.status,
        'payment_method': bill.payment_method or None,
        'customer_name': bill.customer_name,
    })


def menu_list(request):
    items = MenuItem.objects.filter(is_available=True).values(
        'id', 'item_name', 'item_category', 'price'
    )
    return JsonResponse({'menu': list(items)})
