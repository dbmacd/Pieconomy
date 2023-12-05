from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView

from main.models import NutritionalInfo, PieHeaders, PieList, Orders, OrderItems
from .models import CarouselItems, FeaturedItems


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carousel_items'] = CarouselItems.objects.all()
        context['featured_items'] = FeaturedItems.objects.all()
        context['header_items'] = PieHeaders.objects.all()
        return context


class LogInView(LoginView):
    template_name = 'main/login.html'


class LogOutView(LogoutView):
    pass


def register(request):
    if request.method == 'POST':
        user: User
        user = User.objects.create_user(username=request.POST.get('username'),
                                        first_name=request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name'),
                                        email=request.POST.get('email'),
                                        password=request.POST.get('password')
                                        )
        login(request, user)
        return redirect('home')
    return render(request, 'main/register.html')


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user_data'
    template_name = 'main/user_profile.html'

    def get_object(self):
        return self.request.user

def log_out(request):
    logout(request)
    messages.add_message(request, messages.INFO, f'Successfully logged out.')
    return redirect('home')


def forgot_password(request):
    form = PasswordResetForm(None, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'main/forgot_password.html', {'form': form})


def calculator(request):
    pie_list = PieList.objects.all()
    if request.method == "POST":
        selected_pie = PieList.objects.get(id=request.POST["pie_id"])
        cost_of_goods = int(request.POST["cost"])
        calculator_data = {
            'quantity': int(cost_of_goods / selected_pie.cost),
            'pie_cost': cost_of_goods,
            'dataset': f'{int(cost_of_goods / selected_pie.cost)}, {str(cost_of_goods - (selected_pie.cost * int(cost_of_goods / selected_pie.cost)))}',
            'range': range(1, int(cost_of_goods / selected_pie.cost)),
            'can_afford': True if int(cost_of_goods / selected_pie.cost) != 0 else False
        }
        context = {"selected_pie": selected_pie,
                   'loaded': True,
                   'calculator_data': calculator_data}
    else:
        context = {"pie_cost": "",
                   'loaded': False,
                   "selected_pie": None}
    context |= {'pie_list': pie_list}
    return render(request, 'main/calculator.html', context)

class ShopListView(ListView):
    model = PieList
    template_name = 'main/shop.html'
    context_object_name = 'pies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add extra context to display delete buttons based on what the user has ordered
        # User should only have one active order.
        user_order = Orders.objects.filter(is_ordered=False, user_id=self.request.user.id).first()
        if user_order:
            context['order_items'] = OrderItems.objects.filter(order_id=user_order.id)
        else:
            context['order_items'] = None
        return context

class ShopItemDetailView(DetailView):
    model = PieList
    template_name = 'main/detail_view.html'
    context_object_name = 'pie_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add extra context to display nutritional information on the details page
        try:
            context['nutrition'] = NutritionalInfo.objects.get(pie_id=self.object.id)
        except NutritionalInfo.DoesNotExist:
            pass
        return context


def add_order_item(request, item_id: int):
    """
    Adds an item to the current order for the user.
    :param request: Django request object
    :param item_id: Item ID being added
    :return: Either redirects to the register page if user isn't authenticated or redirects
    to the page the user made the request from
    """

    # Get the item from the database and init as an Item Object
    item = PieList.objects.get(id=item_id)

    try:
        # Check if the user is authenticated
        # If they aren't redirect them to the Registration page
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return redirect('register')

    # User is authenticated

    # Get their current open order (as there should only be one)
    order = Orders.objects.filter(is_ordered=False, user_id=user.id).first()

    # If the Order exists
    if order:
        try:
            # Check if the order item is already on the order
            order_item = OrderItems.objects.get(item_id=item.id, order_id=order.id)
        except OrderItems.DoesNotExist:
            order_item = None

        # If the order item exists on the order
        # Increase the quantity and update the last update date/time
        if order_item:
            order_item.quantity += 1
            order_item.save()
            order.last_updated_date_time = datetime.now()
            order.save()

        # if the order item doesn't exist on the order
        # Add it to the order and update the last update date/time
        else:
            order_item = OrderItems(order_id=order, item_id=item)
            order_item.save()
            order.last_updated_date_time = datetime.now()
            order.save()

    # If the Order doesn't exist
    # Create the order and add the order item
    # Redirect the user back to the page they came from.
    else:
        order = Orders(user_id=user)
        order.create_date_time = datetime.now()
        order.save()
        order_item = OrderItems(order_id=order, item_id=item)
        order_item.save()
    return redirect(request.META.get('HTTP_REFERER'))


def remove_order_item(request, item_id: int):
    """
    Removes an item from the current order for the user.
    :param request: Django request object
    :param item_id: Item ID being removed
    :return: Redirects the user to the page they made the request from.
    """

    # Get the item from the database and init as an Item Object
    item = PieList.objects.get(id=item_id)

    # Get the user from the database and init as an User Object
    user = User.objects.get(id=request.user.id)

    # Get their current open order (as there should only be one)
    try:
        order_data = Orders.objects.filter(is_ordered=False, user_id=user.id).first()

        # Order exists
        if order_data:

            # Get the total lines on the order from the database
            order_item_count = OrderItems.objects.filter(order_id=order_data.id).count()

            # Check if the Item is on the order
            order_item = OrderItems.objects.get(item_id=item.id, order_id=order_data.id)

            # Item exists on the order already, reduce its quantity by 1
            if order_item:
                order_item.quantity -= 1

                # If the Item quantity is above 0, save to the DB
                # Update the Orders last updated date and time and save to the DB
                if order_item.quantity > 0:
                    order_item.save()
                    order_data.last_updated_date_time = datetime.now()
                    order_data.save()

                # If the Item quantity is 0, remove the Item from the order.
                # Update the Orders last updated date and time and save to the DB
                else:
                    order_item.delete()
                    order_data.last_updated_date_time = datetime.now()
                    order_data.save()

            # If there are no more items on the order, delete the order.
            if order_item_count == 0:
                order_data.delete()

    # Order doesn't exist, This scenario shouldn't occur.
    # There should be no remove buttons to allow for a user to remove an item off an order
    # that doesn't exist.
    except OrderItems.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER'))


def complete_order(request, order_id):
    completed_order = Orders.objects.get(id=order_id)
    completed_order.last_updated_date_time = datetime.now()
    completed_order.is_ordered = True
    completed_order.save()
    return redirect(request.META.get('HTTP_REFERER'))


def reverse_order(request, order_id):
    reversed_order = Orders.objects.get(id=order_id)
    reversed_order.last_updated_date_time = datetime.now()
    reversed_order.is_ordered = False
    reversed_order.save()
    messages.success(request, f'Order reversed.')
    return redirect(request.META.get('HTTP_REFERER'))


class OrderDetailView(DetailView):
    model = Orders
    template_name = 'main/order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItems.objects.filter(order_id=self.object.id)
        return context


class OrderListView(ListView):
    model = Orders
    context_object_name = 'order_history'
    template_name = 'main/orders.html'
    # TODO Ordering on order history broke when converting to CBV
    def get_object(self):
        return self.model.objects.filter(user_id=self.request.user.id, is_ordered=True).order_by('-last_updated_date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_order'] = self.model.objects.filter(user_id=self.request.user.id, is_ordered=False).first()
        try:
            context['order_items'] = OrderItems.objects.filter(order_id=context['current_order'].id)
        except OrderItems.DoesNotExist:
            context['order_items'] = None
        except AttributeError:
            context['order_items'] = None
        return context

#
# def orders(request):
#     orders_data = Orders.objects.filter(user_id=request.user.id, is_ordered=True).order_by('-last_updated_date_time')
#     current_order = Orders.objects.filter(user_id=request.user.id, is_ordered=False).first()
#     try:
#         current_order_items = OrderItems.objects.filter(order_id=current_order.id)
#     except OrderItems.DoesNotExist:
#         current_order_items = None
#     except AttributeError:
#         current_order_items = None
#     context = {
#         'order_history': orders_data,
#         'current_order': current_order,
#         'order_items': current_order_items
#     }
#     return render(request, 'main/orders.html', context)
