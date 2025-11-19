### Сущность растений ###

```
id (autoincrement)
collection_id (FK to collections)
folder_id (FK to folders)
owner_id (FK to users)
name (text, 100 chars)
genus (text, 50 chars)
species (text, 50 chars)
variety (text, 50 chars)
description (text, 1000 chars)
birth_date (date)
life_status (enum: 'живое', 'погибло')
status (enum: 'активное', 'на обмен', 'подарено', 'продано')
death_date (date)
death_cause (text, 200 chars)
created_at (datetime)
updated_at (datetime)
care_difficulty (enum: 'легкий', 'средний', 'сложный')
light_requirements (enum: 'тень', 'полутень', 'рассеянный свет', 'прямое солнце')
watering_frequency (enum: 'редко', 'умеренно', 'часто')
```

### Сущность журнала событий ###

```
event_id (autoincrement)
plant_id (FK to plants)
event_type (enum: 'полив', 'пересадка', 'удобрение', 'обработка', 'обрезка', 'осмотр', 'фото')
event_date (datetime)
event_description (text, 500 chars)
```

### Сущность состояния ###

```
health_check_id (autoincrement) 
plant_id (FK to plants)
check_date (date)
growth_phase (enum: 'покой', 'вегетация', 'цветение')
pests_detected (text, 200 chars)
diseases_detected (text, 200 chars)
notes (text, 500 chars)
```
