# OW WildHuntLand main RenPy script
init -2 python:
    import sys
    sys.path.append(renpy.loader.transfn("scripts"))
    
init -1 python:
    from random import *
    from whl_engine import *
   
init python:
    pass

# The game starts here.
label start:
    $ session = WildHuntSession(Person("OldHuntsman"))
    show expression "interface/bg_base.jpg" as bg
    call chose_action
    
    return
    
label chose_action:
    $ wd = session.wilderness_name[session.wilderness]
    menu:        
        "Your POW is [session.hero.power]. The [wd] surrounds you."
        "Slaugter [session.captive.name]" if session.captive and "flint chopper" in session.hero.possessions:
            "You get [session.captive.possessions]"
            $ session.hero.possessions.extend(session.captive.possessions)
        "Craft":
            python:
                crafts = session.random_craft()
                cr1 = crafts[0]
                cr2 = crafts[1]
                cr3 = crafts[2]
            menu:    
                "[cr1]":
                    $ txt = Item(cr1).craft(session.hero)
                    "[txt]"
                "[cr2]":
                    $ txt = Item(cr2).craft(session.hero)
                    "[txt]"
                "[cr3]":
                    $ txt = Item(cr3).craft(session.hero)
                    "[txt]"
        "Go deeper in the Wilds" if session.wilderness < 2:
            $ session.wilderness += 1
        "Get out off the Wilds" if session.wilderness > 0:
            $ session.wilderness -= 1           
    
    $ session.captive = None
    call fight         
    return
    
label fight:
    $ session.random_encounter(session.wilderness_name[session.wilderness])
    menu:
        "You encountered: [session.enemy.name] (POW: [session.enemy.power]). Your POW is [session.hero.power]"
        "Fight":
            if session.hero.power < session.enemy.power:
                jump game_over
    
    $ session.captive = session.enemy            
    "You beat [session.enemy.name]"
    call chose_action    
    return
    
label fruits:
    "gathered"
    return
    
label game_over:
    
    menu:
        "GAME OVER":
            pass
        
    return
