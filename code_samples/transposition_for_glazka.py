sph = float(input())
cyl = float(input())
ax = int(input())

cyl_tp = -cyl
ax_tp = ax - 90
sph_tp = sph + cyl

def plus(param):
    if param > 0:
        return '+'
    else:
        return ''

if ax_tp == 0:
    ax_tp = 180
if ax_tp < 0:
    ax_tp = 90 + ax

print(f'Входное значение: Sph {plus(sph)}{sph} Cyl {plus(cyl)}{cyl} Ax {ax}')
print(f'Траспозиция: Sph {plus(sph_tp)}{sph_tp} Cyl {plus(cyl_tp)}{cyl_tp} Ax {ax_tp}')

