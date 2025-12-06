import random
import pandas as pd


def get_smart_tip(df, selected_genera=None, selected_species=None):
    if df.empty:
        return None

    tip_types = ['lifespan', 'death_cause', 'watering', 'seasonality', 'survival_comparison']

    if selected_genera or selected_species:
        tip_types = ['lifespan', 'death_cause', 'watering', 'seasonality']

    tip_type = random.choice(tip_types)

    if tip_type == 'lifespan':
        return _get_lifespan_tip(df, selected_genera, selected_species)

    elif tip_type == 'death_cause':
        return _get_death_cause_tip(df, selected_genera, selected_species)

    elif tip_type == 'watering':
        return _get_watering_tip(df, selected_genera, selected_species)

    elif tip_type == 'seasonality':
        return _get_seasonality_tip(df, selected_genera, selected_species)

    elif tip_type == 'survival_comparison':
        return _get_survival_comparison_tip(df)

    return None


def _get_lifespan_tip(df, selected_genera=None, selected_species=None):
    df = df.copy()
    if 'birth_date' in df.columns and 'death_date' in df.columns:
        df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        df['death_date'] = pd.to_datetime(df['death_date'], errors='coerce')

        mask = df['death_date'].notna() & df['birth_date'].notna()
        df.loc[mask, 'lifespan_years'] = (
                (df.loc[mask, 'death_date'] - df.loc[mask, 'birth_date']).dt.days / 365
        ).round(1)

    dead_plants = df[
        (df['life_status'] == 'погибло') &
        (df['lifespan_years'].notna())
    ]

    if dead_plants.empty:
        return None

    if selected_species:
        valid_species = [s for s in selected_species if s in dead_plants['species'].values]
        if valid_species:
            species = random.choice(valid_species)
            species_plants = dead_plants[dead_plants['species'] == species]
            if not species_plants.empty:
                avg_lifespan = species_plants['lifespan_years'].mean()
                return f"Растения вида {species} в среднем живут {avg_lifespan:.1f} года"

    if selected_genera:
        valid_genera = [g for g in selected_genera if g in dead_plants['genus'].values]
        if valid_genera:
            genus = random.choice(valid_genera)
            genus_plants = dead_plants[dead_plants['genus'] == genus]
            if not genus_plants.empty:
                avg_lifespan = genus_plants['lifespan_years'].mean()
                return f"Растения рода {genus} в среднем живут {avg_lifespan:.1f} года"

    species_counts = dead_plants['species'].value_counts()
    valid_species = species_counts[species_counts >= 2].index.tolist()

    if valid_species:
        species = random.choice(valid_species)
        species_plants = dead_plants[dead_plants['species'] == species]
        avg_lifespan = species_plants['lifespan_years'].mean()
        return f"Растения вида {species} в среднем живут {avg_lifespan:.1f} года"

    genus_counts = dead_plants['genus'].value_counts()
    valid_genera = genus_counts[genus_counts >= 3].index.tolist()

    if valid_genera:
        genus = random.choice(valid_genera)
        genus_plants = dead_plants[dead_plants['genus'] == genus]
        avg_lifespan = genus_plants['lifespan_years'].mean()
        return f"Растения рода {genus} в среднем живут {avg_lifespan:.1f} года"

    avg_lifespan = dead_plants['lifespan_years'].mean()
    return f"Средняя продолжительность жизни растений: {avg_lifespan:.1f} года"


def _get_death_cause_tip(df, selected_genera=None, selected_species=None):
    dead_plants = df[
        (df['life_status'] == 'погибло') &
        (df['death_cause'].notna())
    ]

    if dead_plants.empty:
        return None

    if selected_species:
        valid_species = [s for s in selected_species if s in dead_plants['species'].values]
        if valid_species:
            species = random.choice(valid_species)
            species_plants = dead_plants[dead_plants['species'] == species]
            if not species_plants.empty:
                top_cause = species_plants['death_cause'].mode()
                if not top_cause.empty:
                    return f"Самая частая причина смерти {species} — {top_cause.iloc[0]}"

    if selected_genera:
        valid_genera = [g for g in selected_genera if g in dead_plants['genus'].values]
        if valid_genera:
            genus = random.choice(valid_genera)
            genus_plants = dead_plants[dead_plants['genus'] == genus]
            if not genus_plants.empty:
                top_cause = genus_plants['death_cause'].mode()
                if not top_cause.empty:
                    return f"Самая частая причина смерти растений рода {genus} — {top_cause.iloc[0]}"

    species_counts = dead_plants['species'].value_counts()
    valid_species = species_counts[species_counts >= 2].index.tolist()

    if valid_species:
        species = random.choice(valid_species)
        species_plants = dead_plants[dead_plants['species'] == species]
        top_cause = species_plants['death_cause'].mode()
        if not top_cause.empty:
            return f"Самая частая причина смерти {species} — {top_cause.iloc[0]}"

    genus_counts = dead_plants['genus'].value_counts()
    valid_genera = genus_counts[genus_counts >= 3].index.tolist()

    if valid_genera:
        genus = random.choice(valid_genera)
        genus_plants = dead_plants[dead_plants['genus'] == genus]
        top_cause = genus_plants['death_cause'].mode()
        if not top_cause.empty:
            return f"Самая частая причина смерти растений рода {genus} — {top_cause.iloc[0]}"

    top_cause = dead_plants['death_cause'].mode()
    if not top_cause.empty:
        return f"Самая частая причина смерти растений — {top_cause.iloc[0]}"

    return None


def _get_watering_tip(df, selected_genera=None, selected_species=None):
    """'Растения X поливают раз в Y дней'"""

    if 'watering_interval' not in df.columns:
        return None

    plants_with_data = df[df['watering_interval'].notna()]

    if plants_with_data.empty:
        return None

    if selected_genera:
        valid_genera = [g for g in selected_genera if g in plants_with_data['genus'].values]
        if valid_genera:
            genus = random.choice(valid_genera)
            genus_plants = plants_with_data[plants_with_data['genus'] == genus]
            if not genus_plants.empty:
                avg_interval = genus_plants['watering_interval'].mean()
                return f"Растения рода {genus} поливают раз в {avg_interval:.1f} дней"

    genus_counts = plants_with_data['genus'].value_counts()
    valid_genera = genus_counts[genus_counts >= 2].index.tolist()

    if valid_genera:
        genus = random.choice(valid_genera)
        genus_plants = plants_with_data[plants_with_data['genus'] == genus]
        avg_interval = genus_plants['watering_interval'].mean()
        return f"Растения рода {genus} поливают раз в {avg_interval:.1f} дней"

    avg_interval = plants_with_data['watering_interval'].mean()
    return f"Средний интервал полива растений: {avg_interval:.1f} дней"


def _get_seasonality_tip(df, selected_genera=None, selected_species=None):
    df = df.copy()
    if 'death_date' in df.columns:
        df['death_date'] = pd.to_datetime(df['death_date'], errors='coerce')
        df['death_month'] = df['death_date'].dt.month

    dead_plants = df[
        (df['life_status'] == 'погибло') &
        (df['death_month'].notna())
    ]

    if dead_plants.empty:
        return None

    month_counts = dead_plants['death_month'].value_counts()

    if month_counts.empty:
        return None

    worst_month = month_counts.idxmax()
    worst_count = month_counts.max()

    month_names = {
        1: 'январе', 2: 'феврале', 3: 'марте', 4: 'апреле',
        5: 'мае', 6: 'июне', 7: 'июле', 8: 'августе',
        9: 'сентябре', 10: 'октябре', 11: 'ноябре', 12: 'декабре'
    }

    month_name = month_names.get(worst_month, f"месяце {worst_month}")

    if selected_genera:
        valid_genera = [g for g in selected_genera if g in dead_plants['genus'].values]
        if valid_genera:
            genus = random.choice(valid_genera)
            genus_plants = dead_plants[dead_plants['genus'] == genus]
            if not genus_plants.empty:
                genus_month_counts = genus_plants['death_month'].value_counts()
                if not genus_month_counts.empty:
                    genus_worst = genus_month_counts.idxmax()
                    genus_month_name = month_names.get(genus_worst, f"месяце {genus_worst}")
                    return f"Растения рода {genus} чаще всего погибают в {genus_month_name}"

    return f"Больше всего растений погибает в {month_name} ({worst_count} случаев)"


def _get_survival_comparison_tip(df):
    if df.empty:
        return None

    genus_stats = []

    for genus in df['genus'].dropna().unique():
        genus_df = df[df['genus'] == genus]

        if len(genus_df) >= 3:
            total = len(genus_df)
            alive = (genus_df['life_status'] == 'живое').sum()

            if total > 0:
                survival_rate = (alive / total) * 100
                genus_stats.append({
                    'genus': genus,
                    'rate': survival_rate,
                    'count': total
                })

    if len(genus_stats) < 2:
        return None

    genus_stats.sort(key=lambda x: x['rate'], reverse=True)

    best = genus_stats[0]
    worst = genus_stats[-1]

    if best['genus'] == worst['genus']:
        return None

    if best['count'] < 3 or worst['count'] < 3:
        return None

    if abs(best['rate'] - worst['rate']) < 10:  # Меньше 10% разницы - неинтересно
        return None

    return (
        f"Растения рода {best['genus']} выживают лучше всего ({best['rate']:.1f}%), "
        f"а {worst['genus']} - хуже всего ({worst['rate']:.1f}%)"
    )