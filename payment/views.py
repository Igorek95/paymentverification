from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import PaymentRequisiteForm, PaymentRequestForm
from .models import PaymentRequisite, PaymentRequest
from .serializers import PaymentRequisiteSerializer, PaymentRequestSerializer


def home(request):
    return render(request, 'payment/home.html')


def about(request):
    return render(request, 'payment/about.html')


def contacts(request):
    return render(request, 'payment/contacts.html')


class CreateInvoice(APIView):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        payment_type = request.data.get('payment_type')
        amount = request.data.get('amount')

        existing_request = PaymentRequest.objects.filter(
            requisites__payment_type=payment_type,
            amount=amount,
            status='Pending'
        ).first()

        if existing_request:
            serializer = PaymentRequestSerializer(existing_request)
            return Response(serializer.data, status=status.HTTP_200_OK)

        requisites_data = {
            'payment_type': payment_type,
            'owner_name': kwargs.get('owner_name', 'John Doe'),
            'phone_number': kwargs.get('phone_number', '1234567890'),
            'limit': kwargs.get('limit', 1000.00),
            'user': request.user.id
        }
        requisites_serializer = PaymentRequisiteSerializer(data=requisites_data)
        requisites_serializer.is_valid(raise_exception=True)
        requisites = requisites_serializer.save()

        request_data = {
            'amount': amount,
            'status': 'Pending',
            'requisites': requisites.id,
            'user': request.user.id
        }
        request_serializer = PaymentRequestSerializer(data=request_data)
        request_serializer.is_valid(raise_exception=True)
        payment_request = request_serializer.save()

        response_data = request_serializer.data
        response_data['id'] = payment_request.id

        return Response(response_data, status=status.HTTP_201_CREATED)


class GetInvoiceStatus(APIView):

    def get(self, request, invoice_id, *args, **kwargs):
        try:
            payment_request = PaymentRequest.objects.get(id=invoice_id, user=request.user)
        except PaymentRequest.DoesNotExist:
            return Response({'detail': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PaymentRequestSerializer(payment_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentRequisiteListView(ListView):
    model = PaymentRequisite
    template_name = 'payment/payment_requisite_list.html'
    context_object_name = 'payment_requisites'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if not request.user.is_authenticated:
            return redirect('login')

        if query:
            self.object_list = PaymentRequisite.objects.filter(
                Q(payment_type__icontains=query) | Q(account_type__icontains=query) | Q(owner_name__icontains=query)
            )

        else:
            self.object_list = PaymentRequisite.objects.all()

        context = self.get_context_data()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {'html': render_to_string('payment/payment_requisite_list_ajax.html', context)}
            return JsonResponse(data)

        return self.render_to_response(context)


class PaymentRequisiteDetailView(DetailView):
    model = PaymentRequisite
    template_name = 'payment/payment_requisite_detail.html'
    context_object_name = 'payment_requisite'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)


class PaymentRequisiteCreateView(CreateView):
    model = PaymentRequisite
    form_class = PaymentRequisiteForm
    template_name = 'payment/payment_requisite_form.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment:payment_requisite_detail', kwargs={'pk': self.object.pk})


class PaymentRequisiteUpdateView(UpdateView):
    model = PaymentRequisite
    form_class = PaymentRequisiteForm
    template_name = 'payment/payment_requisite_form.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment:payment_requisite_detail', kwargs={'pk': self.object.pk})


class PaymentRequisiteDeleteView(DeleteView):
    model = PaymentRequisite
    success_url = reverse_lazy('payment:payment_requisite_list')
    template_name = 'payment/payment_requisite_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)


class PaymentRequestListView(ListView):
    model = PaymentRequest
    template_name = 'payment/payment_request_list.html'
    context_object_name = 'payment_requests'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)


class PaymentRequestDetailView(DetailView):
    model = PaymentRequest
    template_name = 'payment/payment_request_detail.html'
    context_object_name = 'payment_request'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)


class PaymentRequestCreateView(CreateView):
    model = PaymentRequest
    form_class = PaymentRequestForm
    template_name = 'payment/payment_request_form.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment:payment_request_detail', kwargs={'pk': self.object.pk})


class PaymentRequestUpdateView(UpdateView):
    model = PaymentRequest
    form_class = PaymentRequestForm
    template_name = 'payment/payment_request_form.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment:payment_request_detail', kwargs={'pk': self.object.pk})


class PaymentRequestDeleteView(DeleteView):
    model = PaymentRequest
    success_url = reverse_lazy('payment:payment_request_list')
    template_name = 'payment/payment_request_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request, *args, **kwargs)
