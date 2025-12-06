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
death_date (date)
death_cause (text, 200 chars)
created_at (datetime)
updated_at (datetime)

```

### Сущность события ###

```
event_id (autoincrement)
plant_id (FK to plants)
event_type (enum: 'полив', 'пересадка', 'удобрение', 'обработка', 'обрезка', ‘болезнь’)
event_date (datetime)
event_description (text, 500 chars)
```
