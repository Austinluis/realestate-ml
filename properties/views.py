from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms as django_forms
from .models import Property

class PropertyForm(django_forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner', 'created_at', 'updated_at']
        widgets = {field: django_forms.TextInput(attrs={'class': 'form-control'})
                   for field in ['title', 'location']}

@login_required
def property_list(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'properties/list.html', {'properties': properties})

@login_required
def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    return render(request, 'properties/detail.html', {'property': prop})

FEATURE_FIELDS = [
    ('mainroad', 'On Main Road?'),
    ('guestroom', 'Guest Room?'),
    ('basement', 'Basement?'),
    ('hotwaterheating', 'Hot Water Heating?'),
    ('airconditioning', 'Air Conditioning?'),
    ('prefarea', 'Preferred Area?'),
]

@login_required
def property_add(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.save()
            messages.success(request, 'Property added successfully.')
            return redirect('property_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PropertyForm()
    return render(request, 'properties/add.html', {'form': form, 'form_features': FEATURE_FIELDS})

@login_required
def property_edit(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('property_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PropertyForm(instance=prop)
    # Build feature list with current values for switch pre-fill
    features_with_values = [
        (fname, flabel, getattr(prop, fname, 'no'))
        for fname, flabel in FEATURE_FIELDS
    ]
    return render(request, 'properties/edit.html', {
        'form': form,
        'property': prop,
        'form_features': FEATURE_FIELDS,
        'form_features_with_values': features_with_values,
    })

@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        prop.delete()
        messages.success(request, 'Property deleted.')
        return redirect('property_list')
    return render(request, 'properties/detail.html', {'property': prop, 'confirm_delete': True})
