from app.schemas import ActionPlanItem, StrategyResponse


def generate_strategy(total_income: float, total_expenses: float) -> StrategyResponse:
    net_balance = round(total_income - total_expenses, 2)
    savings_rate = (
        round(net_balance / total_income * 100, 2) if total_income > 0 else 0.0
    )

    if net_balance <= 0:
        status = "Deficit/Rischio"
        recommendations = [
            ActionPlanItem(
                action_name="Taglio Spese Discrezionali",
                amount=0.0,
                description="Le uscite superano o eguagliano le entrate: elimina temporaneamente le spese non essenziali (ristoranti, abbonamenti, extra) per riportare il bilancio in positivo.",
            ),
            ActionPlanItem(
                action_name="Revisione Budget",
                amount=0.0,
                description="Riequilibria entrate e uscite: analizza ogni categoria e individua dove si concentrano le perdite.",
            ),
        ]
    elif savings_rate < 10:
        status = "Stabile"
        recommendations = [
            ActionPlanItem(
                action_name="Creazione Fondo Emergenza",
                amount=net_balance,
                description=f"Risparmio sotto il 10%: destina l'intero avanzo mensile ({net_balance} €) alla costruzione del fondo di sicurezza (l'obiettivo è 3-6 mesi di spese).",
            ),
        ]
    else:
        status = "Eccellente"
        recommendations = [
            ActionPlanItem(
                action_name="Fondo di Emergenza / Liquidità",
                amount=round(net_balance * 0.5, 2),
                description="Il 50% del risparmio va in liquidità sicura e immediatamente disponibile.",
            ),
            ActionPlanItem(
                action_name="Investimento PAC (es. ETF azionario globale)",
                amount=round(net_balance * 0.3, 2),
                description="Il 30% in un piano di accumulo di lungo periodo (es. ETF globale) per far crescere il capitale.",
            ),
            ActionPlanItem(
                action_name="Spese Guilt-Free (Svago extra)",
                amount=round(net_balance * 0.2, 2),
                description="Il 20% destinato allo svago consapevole: rende il piano sostenibile senza sensi di colpa.",
            ),
        ]

    return StrategyResponse(
        net_balance=net_balance,
        savings_rate=savings_rate,
        status=status,
        recommendations=recommendations,
    )