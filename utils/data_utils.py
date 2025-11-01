import pandas as pd
from io import BytesIO

def sample_maintenance_data(n_machines=6, months=12):
    end = pd.Timestamp.today().normalize()
    start = end - pd.DateOffset(months=months-1)
    periods = pd.date_range(start=start, end=end, freq='MS')
    rows = []
    machines = [f"MAQ-{i:02d}" for i in range(1, n_machines+1)]
    for m in machines:
        mtbf_base = int(100 + (hash(m) % 50))
        for d in periods:
            failures = max(0, int(abs((hash((m,d.month)) % 6) - 1)))
            mtbf = max(20, mtbf_base + (d.month % 7) * 3 - failures * 5)
            mttr = round(2 + (failures * 0.8) + ((hash(d.month) % 3) * 0.5), 1)
            availability = round(90 + (mtbf/200)*10 - failures*0.8, 1)
            cost = round(2000 + failures * 350 + (1000/(mtbf/100+1)), 2)
            rows.append({
                "data_mes": d,
                "maquina": m,
                "falhas": failures,
                "mtbf": mtbf,
                "mttr": mttr,
                "disponibilidade_pct": availability,
                "custo_manutencao": cost
            })
    return pd.DataFrame(rows)

def df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    out = BytesIO()
    with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")
    out.seek(0)
    return out.getvalue()
