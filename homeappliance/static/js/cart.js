// ===== Cart Sidebar =====

const cartSidebar = document.getElementById('cart-sidebar');
const cartOverlay = document.getElementById('cart-overlay');
const cartBtn = document.getElementById('cart-btn');
const cartClose = document.getElementById('cart-close');

function openCart() {
  cartSidebar.classList.add('open');
  cartOverlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCart() {
  cartSidebar.classList.remove('open');
  cartOverlay.classList.remove('open');
  document.body.style.overflow = '';
}

if (cartBtn) cartBtn.addEventListener('click', function(e) {
  e.preventDefault();
  openCart();
});

if (cartClose) cartClose.addEventListener('click', closeCart);
if (cartOverlay) cartOverlay.addEventListener('click', closeCart);

// بستن با کلید Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeCart();
});


// ===== Update quantity =====

document.querySelectorAll('.cart-item-increase').forEach(function(btn) {
  btn.addEventListener('click', function() {
    const itemId = this.dataset.id;
    const input = document.getElementById('qty-' + itemId);
    const newQty = parseInt(input.value) + 1;
    updateQuantity(itemId, newQty);
  });
});

document.querySelectorAll('.cart-item-decrease').forEach(function(btn) {
  btn.addEventListener('click', function() {
    const itemId = this.dataset.id;
    const input = document.getElementById('qty-' + itemId);
    const newQty = parseInt(input.value) - 1;
    if (newQty <= 0) {
      removeItem(itemId);
    } else {
      updateQuantity(itemId, newQty);
    }
  });
});


function updateQuantity(itemId, quantity) {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/cart/update/' + itemId + '/';

  const csrf = document.createElement('input');
  csrf.type = 'hidden';
  csrf.name = 'csrfmiddlewaretoken';
  csrf.value = getCookie('csrftoken');

  const qty = document.createElement('input');
  qty.type = 'hidden';
  qty.name = 'quantity';
  qty.value = quantity;

  form.appendChild(csrf);
  form.appendChild(qty);
  document.body.appendChild(form);
  form.submit();
}

function removeItem(itemId) {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/cart/remove/' + itemId + '/';

  const csrf = document.createElement('input');
  csrf.type = 'hidden';
  csrf.name = 'csrfmiddlewaretoken';
  csrf.value = getCookie('csrftoken');

  form.appendChild(csrf);
  document.body.appendChild(form);
  form.submit();
}


// ===== CSRF Helper =====

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


// ===== اگه sidebar باز بود بعد از reload دوباره باز بشه =====

if (sessionStorage.getItem('cartOpen') === 'true') {
  openCart();
  sessionStorage.removeItem('cartOpen');
}
