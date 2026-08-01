# AI Usage Notes

I used AI (Claude) while building this, mostly to move faster on the boilerplate. Here's an honest breakdown of how.

## What was AI-generated vs. what I did myself

I leaned on AI for the repetitive scaffolding — the initial FastAPI route setup, the Pydantic model classes, and a first draft of the pytest cases. That stuff is fairly standard and there's no point writing it from scratch.

The design decisions were mine though. I decided to go with a JSON file for storage instead of a database, to keep a separate storage layer so the routes stay thin, and I made the calls on how things like IDs and filtering should actually behave. I went through every file after generating it, ran everything locally, and fixed the parts that weren't right.

## What I checked, tested, or changed

A few things I specifically changed or added after reviewing the output:

- The IDs. The first version was basically using the list length to assign IDs, which breaks if you delete something in the middle — you'd end up with duplicate IDs. I switched it to take the max existing ID and add one, so IDs stay unique even after deletes. I added a test for exactly this case (`test_id_survives_delete`) because it's an easy thing to get wrong.

- Rounding on the totals. When I ran the totals test I was getting numbers like 30.000000004 because of how floats add up. So I round to 2 decimals in the storage layer, which makes sense anyway since it's money.

- Deleting something that doesn't exist. Originally it would just quietly do nothing. I made it return a proper 404 instead, since the client should know the delete didn't actually happen.

- Category filtering. I made it case-insensitive so `?category=food` still matches `Food`. Felt like the obvious real-world behaviour and I didn't want it to silently return nothing just because of capitalization.

I validated all of this by running the full test suite (10 tests, all passing) and hitting the endpoints through the Swagger UI at `/docs`.

## What the AI suggested that I didn't use

It suggested using SQLite for storage at one point. I skipped it — the assignment said no database was needed, and a JSON file keeps the whole thing self-contained so it just runs on a clean checkout without any setup. I also kept the scope tight and didn't add things like auth that weren't asked for, since that would just be extra complexity for no reason here.
