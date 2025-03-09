from django import forms


class StockBuySellForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label="Quantity",
        widget=forms.NumberInput(
            attrs={"placeholder": "Enter quantity", "id": "quantity"}
        ),
    )
