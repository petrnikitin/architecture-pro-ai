"""
Дополнительные документы для базы знаний Cyber Nexus
Добавляет ещё 11+ документов для достижения требуемых 30+
"""

import sys
from pathlib import Path

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


ADDITIONAL_DOCS = {
    "characters": {
        "Gorvan.md": """# Gorvan

## Overview
Gorvan is a Taurian warrior and co-pilot of the Quantum Drifter. Standing over 2 meters tall with brown fur, he is Drake Vortex's loyal friend and partner.

## Background
Born on Sylvaros, Gorvan was exiled after a dispute with other Taurians. He wandered the Nexus Realm until meeting Drake Vortex, forming a lifelong partnership.

## Skills
Despite his fearsome appearance, Gorvan is an excellent mechanic, navigator, and bowcaster marksman. His strength and combat prowess have saved the crew countless times.

## Role in Liberation
Gorvan fought in numerous battles including:
- Rescue of Lyra Zenith
- Battle of Yavin
- Battle of Frosthold
- Battle of Verdant Moon

## Personal Life
Gorvan's loyalty to his friends is unwavering. After the war, he continued flying with Drake, occasionally taking solo missions for the New Unity Council.

## Cultural Significance
Gorvan helped change perceptions of Taurians in the Nexus Realm, showing they were more than just fierce warriors.
""",

        "Unit-7X.md": """# Unit-7X

## Overview
Unit-7X is an astromech synth unit who served the Unity Council, the Liberation Front, and later the New Unity Council. Known for his resourcefulness and bravery, he has been involved in many pivotal events.

## Design
Unit-7X is a dome-headed synth unit standing about 1 meter tall. He communicates through electronic beeps and whistles, though other synth units and some organic beings can understand him.

## Capabilities
- Starship repair and maintenance
- Computer interface and hacking
- Navigation and astrogation
- Storage of vast amounts of data
- Holographic projection

## History
Unit-7X served Senator Amidala during the Synthetic Wars. After Order 66, he was entrusted with Kael Novarek's safety, later delivering Thal Kyros's message.

## Adventures
The synth unit has been through:
- Escape from Nexara Central
- Journey to Aridus Prime
- Battle of Yavin (as Luke's astromech)
- Rescue of Drake Vortex on Frosthold
- Mission to Verdant Moon

## Companion
Often paired with Cypher-9, their contrasting personalities (brave vs cautious) create an iconic duo.

## Legacy
Unit-7X became one of the most famous synth units in history, inspiring a new generation of astromech designs.
""",

        "Cypher-9.md": """# Cypher-9

## Overview
Cypher-9 is a protocol synth unit fluent in over 6 million forms of communication. Built to serve as a diplomat's assistant, he often finds himself in dangerous situations he'd rather avoid.

## Design
Cypher-9 has a humanoid frame with gold-colored plating. He stands about 1.7 meters tall and moves with a distinctive gait.

## Personality
Known for his anxious and protocol-obsessed nature, Cypher-9 is nonetheless loyal to his companions. He often voices concerns about dangerous situations while still participating.

## Capabilities
- Translation of 6+ million languages
- Diplomatic protocol knowledge
- Etiquette and cultural awareness
- Limited combat abilities
- Can interface with computer systems

## History
Created on Nexara Central, Cypher-9 served Senator Amidala. After her death, he was passed to Lyra Zenith, serving the Liberation Front throughout the war.

## Notable Moments
- Translating for diverse alien species
- Discovering Void Core vulnerabilities in Imperial databases
- Negotiating with the Sylvani on Verdant Moon
- Surviving being dismantled and reassembled multiple times

## Partnership with Unit-7X
The two synth units have an odd-couple relationship, with Cypher-9's cautious nature contrasting Unit-7X's boldness. Despite constant bickering, they are inseparable.
""",

        "Nova_Starwind.md": """# Nova Starwind

## Overview
Nova Starwind is a powerful Flux-sensitive individual who played a key role in the final defeat of the Voidborn remnants. Initially untrained, she became one of the most powerful Synthari of the new generation.

## Origins
Nova grew up as a scavenger on Wasteland Sigma, unaware of her heritage or Flux sensitivity. She discovered her abilities when finding Aric Flameborn's Plasma Blade.

## Training
Under Kael Novarek's guidance, Nova learned to harness the Synth Flux. Her training was unorthodox, combining Synthari teachings with practical combat experience.

## Abilities
Nova demonstrated exceptional talents:
- Rapid learning of Flux techniques
- Strong connection to both Radiant Flow and Void Resonance
- Natural pilot and mechanic
- Combat skills with Plasma Blade and blaster

## Key Battles
- Oblivion Station assault
- Defeat of Kain Shadowstrike
- Final confrontation with residual Voidborn forces

## Legacy
Nova helped rebuild the Synthari Order, emphasizing balance and avoiding the mistakes of the past. She advocated for allowing Synthari to form attachments and families.

## Philosophy
She believed the old Synthari Order's strict rules contributed to Aric's fall, and that a more balanced approach was needed for the new Order.
""",

        "Kain_Shadowstrike.md": """# Kain Shadowstrike

## Overview
Kain Shadowstrike, born as Ben Solo, was a Voidlord who served the Prime Covenant. Son of Lyra Zenith and Drake Vortex, he fell to the Void Resonance despite his parents' efforts.

## Early Life
Born with powerful Flux abilities, Ben was sent to train with Kael Novarek. However, he felt drawn to the Void Resonance, influenced by echoes of Lord Umbral's power.

## Fall
Believing Kael planned to eliminate him, Ben destroyed the new Synthari Temple and fled. He became Kain Shadowstrike under the guidance of Shadow Sovereign Snoke.

## Abilities
Kain was immensely powerful:
- Telekinesis without gesture
- Ability to freeze objects and people mid-motion
- Mind reading
- Flux rage enhancements

## Internal Conflict
Unlike previous Voidborn, Kain struggled with the Radiant Flow within him. This internal conflict defined his character and ultimately led to his redemption.

## Redemption
In his final moments, Kain rejected the Void Resonance, helping Nova Starwind defeat Shadow Sovereign. He died as Ben Solo, redeemed like his grandfather before him.

## Legacy
His story became a warning about the dangers of fear and isolation, but also a testament to the possibility of redemption.
""",
    },

    "organizations": {
        "Prime_Covenant.md": """# Prime Covenant

## Overview
The Prime Covenant was a military organization that emerged from the remnants of the Nexus Dominion decades after its fall. Led by Shadow Sovereign Snoke, it sought to restore authoritarian rule.

## Formation
Built in the Unknown Regions using surviving Dominion resources and personnel, the Covenant grew in secret for years before revealing itself.

## Military Forces
- Covenant Enforcers: Elite soldiers with advanced training
- Nexus Interceptor Mark II: Updated starfighters
- Titan Cruiser Supremacy: Massive flagship
- Oblivion Station: Mobile superweapon

## Leadership
- Shadow Sovereign: Supreme leader
- Kain Shadowstrike: Enforcer and Voidlord
- General Hux: Military commander
- Captain Phasma: Stormtrooper commander

## Goals
The Covenant aimed to:
- Destroy the New Unity Council
- Eliminate remaining Synthari
- Restore order through strength
- Complete what the Dominion began

## Downfall
The Covenant was defeated when Oblivion Station was destroyed and Shadow Sovereign was killed. Remaining forces scattered or surrendered.
""",

        "Free_Coalition.md": """# Free Coalition

## Overview
The Free Coalition was a military force organized to oppose the Prime Covenant. Led by veterans of the Liberation Front, it defended the New Unity Council.

## Formation
When the Covenant revealed itself, General Lyra Zenith organized veteran Liberators and new volunteers to resist the threat.

## Forces
- Veteran Liberation Front personnel
- Delta Wing squadrons
- Frigate fleet
- Ground troops trained by former Liberators

## Leadership
- General Lyra Zenith: Overall commander
- Admiral Ackbar: Fleet commander
- Poe Dameron: Squadron leader
- Finn: Ground forces commander

## Key Operations
- Defense of Unity Prime
- Destruction of Oblivion Station
- Liberation of Covenant-occupied worlds
- Final assault on the Covenant fleet

## Victory
The Coalition achieved victory through clever tactics, sacrifice, and the redemption of Kain Shadowstrike. Many Coalition members transitioned to peacekeeping roles afterward.
""",

        "Synthetic_Legion.md": """# Synthetic Legion

## Overview
The Synthetic Legion was the military force of the Unity Council during the Synthetic Wars. They were genetically engineered soldiers created from a single template.

## Creation
The Legion was commissioned by the Unity Council after war broke out with the Fracture Syndicate. Created on Aqualis, they were designed for absolute loyalty.

## Design
Each soldier was cloned from bounty hunter Jango Fett. They were:
- Genetically enhanced for combat
- Trained from birth
- Equipped with standardized armor
- Conditioned to follow orders

## Structure
Organized into divisions led by Synthari generals, the Legion fought across the Nexus Realm. Different units had specialized training (pilots, commandos, ARCs).

## Order 66
The Legion's loyalty was exploited when Lord Umbral activated Order 66, commanding them to eliminate their Synthari commanders. This betrayal nearly destroyed the Synthari Order.

## Legacy
After the war, clones were phased out and replaced with recruited soldiers. Some clones removed their control chips and lived peaceful lives, while others joined the Liberation Front.

## Notable Clones
- Captain Rex: Removed chip, joined Liberation
- Commander Cody: Led Synthari betrayal
- Bad Batch: Defective clones who resisted Order 66
""",
    },

    "planets": {
        "Murkvale.md": """# Murkvale

## Overview
Murkvale is a remote swamp planet in the Outer Rim where Grand Archon Zeph Nexar lived in exile for decades.

## Environment
The planet is covered in dense swamps, bogs, and marshlands. Gnarled trees and thick fog make navigation difficult. The air is humid and filled with strange sounds.

## Wildlife
Diverse creatures inhabit the swamps:
- Bog serpents: Large reptilian predators
- Swamp slugs: Slow-moving herbivores
- Spider-crabs: Aggressive arachnids
- Various fish and amphibians

## Force Connection
Murkvale has an unusually strong connection to the Synth Flux. The swamp itself seems to be aware, testing those who enter.

## Zeph's Exile
Grand Archon Zeph chose Murkvale for its remoteness and strong Flux connection. He lived in a simple dwelling, meditating and maintaining his connection to the Flux.

## Kael's Training
When Kael Novarek arrived, Zeph initially refused to train him. Only after seeing Kael's determination did Zeph agree, teaching him advanced Flux techniques.

## Current Status
After Zeph's death, Murkvale was left undisturbed. Some Synthari pilgrims visit to meditate in locations where Zeph trained students.
""",

        "Wasteland_Sigma.md": """# Wasteland Sigma

## Overview
Wasteland Sigma is a remote desert planet covered in wreckage from a major space battle decades ago. It became home to scavengers and refugees.

## History
The planet was the site of a massive battle during the Nexus Liberation War. The wrecks of countless ships crashed on the surface, never salvaged due to the planet's remoteness.

## Environment
Harsh desert climate with extreme heat. The surface is littered with:
- Star Destroyer wrecks
- Crashed fighters
- Destroyed walkers
- Ancient settlements

## Inhabitants
Most inhabitants are scavengers who salvage parts from wrecks to trade for food and supplies. Life is hard, and exploitation is common.

## Nova's Origins
Nova Starwind grew up as a scavenger, exploring ship wrecks and selling parts. This harsh environment forged her resilience and resourcefulness.

## Strategic Importance
Despite its desolation, Wasteland Sigma holds valuable technology and data in the wrecks. Various factions search for specific items hidden in the debris.

## Current Status
The planet remains largely lawless, though the New Unity Council has established a small outpost to prevent exploitation and help resettle refugees.
""",

        "Seraphina.md": """# Seraphina

## Overview
Seraphina is a lush, beautiful planet known for its peaceful culture and stunning architecture. It was the homeworld of Queen Sera Astralis.

## Geography
The planet features:
- Rolling green plains
- Crystal-clear lakes
- Elegant cities with classical architecture
- Underwater Gungan cities

## Culture
Seraphina's culture emphasizes:
- Diplomacy and peace
- Arts and education
- Democratic governance
- Environmental preservation

## Government
Seraphina has an elected monarch who works with elected officials. Queen Sera Astralis represented this tradition of servant leadership.

## Synthetic Wars
Seraphina was invaded during the Synthetic Wars, leading to the Battle of Seraphina. This battle showcased the bravery of the Synthetic Legion and Synthari.

## After the War
Following the war, Seraphina rebuilt and became a center for cultural exchange and education. The planet remains a symbol of peace and beauty in the Nexus Realm.

## Legacy
Sera Astralis's legacy lives on through her children, Kael and Lyra, who both became heroes of the Liberation.
""",

        "Infernis.md": """# Infernis

## Overview
Infernis is a volcanic planet with rivers of lava and a harsh, toxic atmosphere. It served as the site of Aric Flameborn's transformation into Xarn Velgor.

## Environment
The planet is covered in:
- Active volcanoes
- Lava rivers and falls
- Toxic gas clouds
- Black sand shores
- Mining facilities

## Fracture Syndicate
Infernis was home to Syndicate mining operations. The planet's extreme conditions made it an ideal place for hidden facilities.

## Battle of Infernis
The final confrontation of the Synthetic Wars occurred here. Thal Kyros and Aric Flameborn dueled while the facility collapsed around them.

## Aric's Fall
Defeated and burned by lava, Aric was rescued by Lord Umbral. His transformation into the cybernetic Xarn Velgor occurred in a medical facility above Infernis.

## Symbolism
Infernis represents destruction and rebirth. Just as Aric "died" there, Xarn Velgor was "born" from the ashes.

## Current Status
After the Dominion's fall, Infernis was abandoned. Some dark side cultists visit the planet, seeking to connect with echoes of the Void Resonance.
""",
    },

    "technology": {
        "Warp_Core.md": """# Warp Core

## Overview
The Warp Core (Hyperdrive) is technology that allows starships to travel faster than light by entering the Quantum Void - an alternate dimension parallel to normal space.

## Function
Warp Cores work by:
1. Generating a massive amount of energy
2. Creating a field that shifts the ship into the Quantum Void
3. Allowing near-instantaneous travel across vast distances
4. Returning to normal space at the destination

## Classes
Warp Cores are rated by class number:
- Class 0.5: Military-grade, extremely fast (like Quantum Drifter)
- Class 1: Standard fast hyperdrive
- Class 2: Commercial transport speed
- Class 3+: Slow, backup drives

## Navigation
Quantum Void travel requires precise calculations. Established routes are mapped, but new routes require careful calculation to avoid hitting celestial objects.

## History
Warp Core technology has existed for millennia. Improvements in speed and safety have been incremental but significant.

## Safety
Quantum Void accidents are rare but catastrophic. Ships that miscalculate can collide with objects or become lost in the Void.

## Strategic Importance
Control of Warp Core technology is crucial for any major power in the Nexus Realm. The ability to move forces quickly determines victory in war.
""",

        "Titan_Walker.md": """# Titan Walker

## Overview
The Titan Walker (All Terrain Armored Transport) is a four-legged combat walker used by the Nexus Dominion and later the Prime Covenant.

## Specifications
- Height: 22.5 meters
- Length: 20 meters
- Crew: 5 (pilot, co-pilot, gunner, commander, engineer)
- Passengers: 40 Dominion Guards
- Weapons: Heavy laser cannons, medium blasters

## Design
The walker's four legs allow it to traverse rough terrain. Heavily armored on the front and sides, but vulnerable to attacks on the legs or rear.

## Tactical Use
Titan Walkers were designed for:
- Planetary assault
- Intimidation of enemy forces
- Transport of troops
- Heavy fire support

## Battle of Frosthold
Titan Walkers spearheaded the assault on Echo Base. Their armor resisted Liberation Front weapons, requiring creative tactics to defeat them.

## Weaknesses
- Slow movement speed
- Vulnerable underbelly and rear armor
- Leg joints can be targeted with cables
- Top hatch vulnerable to grenades

## Variants
- Titan Walker II: Upgraded armor and weapons (Prime Covenant)
- Scout Strider: Smaller, faster two-legged variant
- Titan Swimmer: Aquatic assault variant

## Legacy
The sight of Titan Walkers became synonymous with Dominion oppression. After the war, many were decommissioned or retrofitted for civilian use.
""",
    },
}


def generate_additional_documents():
    """Генерирует дополнительные документы"""
    base_dir = Path("knowledge_base/processed")

    print("🚀 Добавляю дополнительные документы в базу знаний...\n")

    total_docs = sum(len(docs) for docs in ADDITIONAL_DOCS.values())
    current = 0

    for category, documents in ADDITIONAL_DOCS.items():
        category_dir = base_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        print(f"📁 Категория: {category}")

        for filename, content in documents.items():
            current += 1
            file_path = category_dir / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content.strip())

            print(f"   [{current}/{total_docs}] ✅ {filename}")

        print()

    print(f"✅ Добавлено {total_docs} документов!")

    # Общая статистика
    total_files = sum(1 for _ in base_dir.rglob('*.md'))
    print(f"\n📊 Всего документов в базе знаний: {total_files}")


if __name__ == "__main__":
    generate_additional_documents()
    print("\n✅ База знаний Cyber Nexus обновлена!")
