# GameOfTESI-2

Dataset for Game of Thrones and Natural Language Processing

Folder structures:
    
    episodesJSON:
        season_1:
            a_golden_crown.json
            baelor.json
        season_2:
            a_man_without_honor.json
            blackwater.json
        ...
    
    
    episodesTXT:
        season_1:
            a_golden_crown.txt
            baelor.txt
        season_2:
            a_man_without_honor.txt
            blackwater.txt
        ...
    
    episodesRAW:
        season_1:
            a_golden_crownRAW.txt
            baelorRAW.txt
        season_2:
            a_man_without_honorRAW.txt
            blackwaterRAW.txt
        ...
    
    convertRAW_JSON:
        main.py
            "You can execute main.py to transform the raw.txt file (episodesRAW folder) into .json file (episodesJSON folder)"
            
    convertJSON_TXT:
        main.py
                "You can execute main.py to transform the .json file (episodesJSON folder) into .txt file (episodesTXT folder)"

File structures:

    JSON:
        "Dictionary with keys that represents meta-informations about the episode."
        List of keys:
            - title
            - season
            - episode
            - date
            - authors
            - directors
            - info
            - plot
            - summary
            - firsts
            - deaths
            - cast
            
    TXT:
        <key1_path in json file>
        sentence 1.
        sentence 2.
        sentence 3.
    
        <key2_path in json file>
        sentence 1.
        sentence 2.
        ...
        
    RAW:
        "Raw text from http: ..."
