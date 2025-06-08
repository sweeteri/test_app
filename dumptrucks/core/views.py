from django.views import View
from django.shortcuts import render
from .models import Truck, Stock, UnloadPoint
from .forms import CoordinateForm
from .utils import is_inside_stock


class TruckUnloadView(View):
    template_name = 'core/index.html'

    def get_truck_forms(self):
        trucks = Truck.objects.all()
        forms = []
        for truck in trucks:
            unload = UnloadPoint.objects.filter(truck=truck).first()
            coord = f"{unload.x} {unload.y}" if unload else ''
            form = CoordinateForm(initial={'coordinates': coord}, prefix=str(truck.id))
            forms.append((truck, form))
        return forms

    def get(self, request):
        stock = Stock.objects.first()
        context = {
            'truck_forms': self.get_truck_forms(),
            'stock_before': stock.volume if stock else 0,
            'show_results': False,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        trucks = Truck.objects.all()
        any_unloaded = False

        for truck in trucks:
            field_name = f'{truck.id}-coordinates'
            coords = request.POST.get(field_name)

            if coords and coords.strip():
                try:
                    x, y = map(float, coords.strip().split())

                    UnloadPoint.objects.update_or_create(truck=truck, defaults={'x': x, 'y': y})
                except ValueError as e:

                    UnloadPoint.objects.filter(truck=truck).delete()
            else:

                UnloadPoint.objects.filter(truck=truck).delete()

        stock = Stock.objects.first()
        total_mass = stock.volume if stock else 0
        si_mass = total_mass * (stock.sio2_pct / 100) if stock else 0
        fe_mass = total_mass * (stock.fe_pct / 100) if stock else 0

        for truck in trucks:
            unload = UnloadPoint.objects.filter(truck=truck).first()
            print(unload)
            if unload and is_inside_stock(unload.x, unload.y):
                any_unloaded = True
                total_mass += truck.current_weight
                si_mass += truck.current_weight * truck.sio2_pct / 100
                fe_mass += truck.current_weight * truck.fe_pct / 100

        context = {
            'truck_forms': self.get_truck_forms(),
            'stock_before': stock.volume if stock else 0,
            'show_results': any_unloaded,
        }
        if any_unloaded:
            si_pct = round(si_mass / total_mass * 100, 2)
            fe_pct = round(fe_mass / total_mass * 100, 2)
            context.update({
                'stock_after': round(total_mass, 2),
                'new_sio2': si_pct,
                'new_fe': fe_pct,
            })

        return render(request, self.template_name, context)
