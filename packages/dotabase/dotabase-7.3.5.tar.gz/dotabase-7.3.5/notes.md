
https://packaging.python.org/tutorials/distributing-packages/
https://stackoverflow.com/questions/26737222/pypi-description-markdown-doesnt-work?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
# update
```
rm -rf dist/
rm -rf dotabase.egg-info/
python setup.py sdist
twine upload --repository pypi dist/*
```

sqlite3 dotabase.db ".dump" > dotabase.db.sql

BoldCrypticPistachioUncleNox

RoundImpossibleAnacondaRalpherZ




-include dotabase.db
+include dotabase/dotabase.db

dota_english_file
UnicodeDecodeError: 'utf-16-le' codec can't decode byte 0x0a in position 2714890: truncated data
```
Traceback (most recent call last):
  File "builder.py", line 72, in <module>
    build_dotabase()
  File "builder.py", line 57, in build_dotabase
    chat_wheel.load()
  File "C:\dev\projects\dotabase-builder\builder_parts\chat_wheel.py", line 51, in load
    data = valve_readfile(config.vpk_path, paths['dota_english_file'], "kv", encoding="UTF-16")["lang"]["Tokens"]
  File "C:\dev\projects\dotabase-builder\valve2json.py", line 275, in valve_readfile
    text = f.read()
  File "C:\Users\dillerm\AppData\Local\Programs\Python\Python36\lib\codecs.py", line 321, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
  File "C:\Users\dillerm\AppData\Local\Programs\Python\Python36\lib\encodings\utf_16.py", line 61, in _buffer_decode
    codecs.utf_16_ex_decode(input, errors, 0, final)
UnicodeDecodeError: 'utf-16-le' codec can't decode byte 0x0a in position 2714890: truncated data
```

# stuff for mistwoods update
- DOTA_Tooltip_ability_weaver_the_swarm_shard_description  ("HasShardUpgrade": "1",)
- DOTA_Tooltip_ability_tinker_laser_scepter_description    ("HasScepterUpgrade": "1",)
- 


/panorama/images/hud/reborn/aghsstatus_scepter_on_psd.png
/panorama/images/hud/reborn/aghsstatus_shard_on_psd.png


MAYBE ADD IsObsolete FOR FUTURE
MAYBE ADD PROP IS_OBTAINABLE (purchasable/craftable/droppable(aegis)/neutral/nonobsolete)



NOW:
- UPDATE ICONS/IMAGES
- FIX SHARD STUFF IN MANGO

# fixed
- arcane blink recipe has a * in it
- aghs stuff for multiple people missing (skywrath, oracle) write script to check


# dotabase fixes
- special attributes for shards? (see pudge)


fmpeg -ss "$screenshot_time" -i $(youtube-dl -f 22 --get-url "$youtube_url") -vframes 1 -q:v 2 "$output_file"




# patch infos
- number (datafeed)
- timestamp (datafeed)
- custom website url (datafeed)
- wiki url
- dota url



# todo
- add emoticons from new teams thing
- add herochatwheel {tier} criteria for responses ( mayeb theese sould also have the vsnd id?)




same in dota:
fMOVE SPEED PER INSTANCE:
Puck attacks all enemies within its attack range + 200 every time it phase shifts.



weirdly updated in dota:
"-%value% Rip Tide Hits" - this is the one we have weird shit goin on with in the data




Flux ++ talent

LEGION THING


SPEED OF VSND FILE READING

AGHS CHECK ALL



# technical
- sb ulti
- shaker abilities
- brstle hairball
- decoy bushwack
- nimbus lightnignbolt
