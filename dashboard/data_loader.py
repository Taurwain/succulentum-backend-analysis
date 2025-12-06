import sqlite3
import pandas as pd


def get_db_connection():
    conn = sqlite3.connect('db/succulentum.db')
    conn.row_factory = sqlite3.Row
    return conn


def load_plants_data():
    conn = get_db_connection()

    query = """
        SELECT 
            p.id, p.collection_id, p.folder_id, p.owner_id,
            p.name, p.genus, p.species, p.variety, p.description,
            p.birth_date, p.life_status, p.death_date, p.death_cause,
            p.created_at, p.updated_at,
            COUNT(DISTINCT CASE WHEN e.event_type = 'полив' THEN e.event_id END) as watering_count,
            COUNT(DISTINCT e.event_id) as total_events
        FROM plants p
        LEFT JOIN plant_events e ON p.id = e.plant_id
        GROUP BY p.id
    """

    plants_df = pd.read_sql_query(query, conn)

    events_query = """
        SELECT plant_id, event_type, event_date 
        FROM plant_events 
        WHERE event_type = 'полив'
        ORDER BY plant_id, event_date
    """

    events_df = pd.read_sql_query(events_query, conn)
    conn.close()

    watering_intervals = {}
    if not events_df.empty:
        events_df['event_date'] = pd.to_datetime(events_df['event_date'])
        events_df = events_df.sort_values(['plant_id', 'event_date'])

        for plant_id, group in events_df.groupby('plant_id'):
            if len(group) > 1:
                intervals = group['event_date'].diff().dt.days.dropna()
                if not intervals.empty:
                    watering_intervals[plant_id] = intervals.mean()

    plants_df['watering_interval'] = plants_df['id'].map(watering_intervals)

    plants_df['lifespan_days'] = None
    mask = plants_df['life_status'] == 'погибло'
    plants_df.loc[mask, 'lifespan_days'] = (
            pd.to_datetime(plants_df.loc[mask, 'death_date']) -
            pd.to_datetime(plants_df.loc[mask, 'birth_date'])
    ).dt.days

    plants_df['death_month'] = None
    plants_df.loc[mask, 'death_month'] = pd.to_datetime(
        plants_df.loc[mask, 'death_date']
    ).dt.month

    return plants_df


def get_filter_options(plants_df):
    all_genera = sorted(plants_df['genus'].dropna().unique())
    all_species = sorted(plants_df['species'].dropna().unique())
    all_varieties = sorted(plants_df['variety'].dropna().unique())

    return all_genera, all_species, all_varieties
