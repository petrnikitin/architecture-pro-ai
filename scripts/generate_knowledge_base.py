"""
Генератор уникальной базы знаний Cyber Nexus
(альтернатива скачиванию из фандома)

Создаёт 30+ документов с заменёнными терминами на основе
известных фактов о Star Wars.
"""

import sys
import json
from pathlib import Path

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# Шаблоны документов с уже заменёнными терминами
DOCUMENTS = {
    "characters": {
        "Xarn_Velgor.md": """# Xarn Velgor

## Overview
Xarn Velgor, formerly known as Aric Flameborn, was a Voidlord of the Voidborn who served the Nexus Dominion. Once a powerful Synthari Archon, he fell to the Void Resonance and became one of the most feared figures in the Nexus Realm.

## Early Life
Born on Aridus Prime, Aric Flameborn was discovered by Synthari Archon Thal Kyros at a young age. He showed exceptional talent with the Synth Flux and quickly rose through the ranks of the Synthari Order.

## Fall to the Void Resonance
Driven by fear of loss and manipulated by Lord Umbral, Aric turned to the Void Resonance. He pledged himself to the Voidborn and took the name Xarn Velgor. He led the Dominion forces in hunting down the remaining Synthari after the execution of Order 66.

## Abilities
Xarn Velgor was a master of Plasma Blade combat and wielded the Synth Flux with unmatched power. His cybernetic suit sustained his damaged body and enhanced his already formidable abilities.

## Legacy
Despite his dark path, Xarn Velgor ultimately redeemed himself by destroying Lord Umbral and saving his son, Kael Novarek, bringing balance to the Synth Flux.
""",

        "Kael_Novarek.md": """# Kael Novarek

## Overview
Kael Novarek was a legendary Synthari Archon who played a crucial role in the destruction of the Void Core and the fall of the Nexus Dominion. Son of Aric Flameborn and Sera Astralis, he was one of the last trained Synthari.

## Early Life
Raised on Aridus Prime by his aunt and uncle, Kael grew up unaware of his true heritage. His life changed when he received a message from Zeph Nexar, delivered by Unit-7X and Cypher-9, revealing his destiny.

## Training
Under the guidance of Thal Kyros and later Zeph Nexar, Kael learned to harness the Synth Flux. Despite limited training, his natural abilities and connection to the Flux were extraordinarily strong.

## Key Achievements
- Destroyed the Void Core, the Dominion's ultimate weapon
- Helped found the New Unity Council
- Trained a new generation of Synthari, including Nova Starwind
- Confronted and redeemed his father, Xarn Velgor

## Legacy
Kael Novarek became a symbol of hope for the Nexus Realm, proving that even in the darkest times, the Radiant Flow of the Synth Flux could prevail.
""",

        "Lyra_Zenith.md": """# Lyra Zenith

## Overview
Lyra Zenith was a leader of the Liberation Front and key figure in the overthrow of the Nexus Dominion. Born as a princess of Celestia Nova, she dedicated her life to fighting tyranny and oppression.

## Early Life
Born to the royal family of Celestia Nova, Lyra was raised in a culture of diplomacy and peace. When her homeworld was destroyed by the Void Core, she channeled her grief into leading the Liberation Front.

## Role in the Liberation
Lyra served as a diplomat, soldier, and eventually a council member in the resistance against the Dominion. Her strategic mind and diplomatic skills were crucial to forming alliances across the Nexus Realm.

## Personal Life
She formed a close bond with Drake Vortex, eventually marrying him. She also discovered that Kael Novarek was her twin brother, separated at birth for their safety.

## Abilities
While not trained as a Synthari, Lyra possessed latent Flux sensitivity. She was an excellent marksman, skilled pilot, and charismatic leader.

## Legacy
After the fall of the Dominion, Lyra became a founding member of the New Unity Council, working to restore peace and democracy to the Nexus Realm.
""",

        "Drake_Vortex.md": """# Drake Vortex

## Overview
Drake Vortex was a smuggler and captain of the legendary starship Quantum Drifter. Despite his roguish exterior, he became a hero of the Liberation Front and a key figure in the defeat of the Nexus Dominion.

## Background
Born on Corellia, Drake lived a life on the fringes of society. Along with his co-pilot Gorvan, he made his living smuggling goods across the Nexus Realm, often running from creditors.

## Joining the Liberation
Initially motivated by money, Drake agreed to transport Thal Kyros, Kael Novarek, and Unit-7X to Celestia Nova. This decision set him on a path that would make him a hero of the Liberation.

## Key Moments
- Rescued Lyra Zenith from the Void Core
- Piloted the Quantum Drifter in the battle that destroyed the Void Core
- Saved Kael Novarek during the Battle of Frosthold
- Led the strike team that disabled the Void Core's shields

## Skills
Drake was one of the best pilots in the Nexus Realm, with exceptional reflexes and an intuitive understanding of starship mechanics. He was also a skilled marksman and tactician.

## Personal Life
Drake eventually married Lyra Zenith and settled down, though he never lost his adventurous spirit. He and Gorvan continued occasional missions for the New Unity Council.
""",

        "Thal_Kyros.md": """# Thal Kyros

## Overview
Thal Kyros was a legendary Synthari Archon and general who served the Unity Council during the Synthetic Wars. He later mentored Aric Flameborn and, decades later, Kael Novarek.

## Early Life
Born on Stewjon, Thal was trained in the ways of the Synthari from childhood. He became known for his wisdom, diplomacy, and exceptional skill with the Synth Flux.

## The Synthetic Wars
During the Synthetic Wars, Thal was a general in the Synthetic Legion. He fought alongside Aric Flameborn and formed a deep bond with him, considering him like a brother.

## Exile and Return
After the rise of the Dominion and the fall of the Synthari, Thal went into hiding on Aridus Prime. He watched over young Kael Novarek from afar, waiting for the right time to reveal his heritage.

## Sacrifice
Thal gave his life in a duel with Xarn Velgor aboard the Void Core, allowing Kael and his companions to escape. Before his death, he became one with the Synth Flux, continuing to guide Kael from beyond.

## Legacy
Thal Kyros was remembered as one of the greatest Synthari of his era, embodying the principles of wisdom, compassion, and selflessness.
""",

        "Zeph_Nexar.md": """# Zeph Nexar

## Overview
Zeph Nexar was one of the most powerful and wise Synthari Archons in history. Despite his small stature, he was a formidable warrior and teacher who trained Synthari for over 800 years.

## History
For centuries, Zeph served as the Grand Archon of the Synthari Order, teaching countless initiates in the ways of the Synth Flux. His wisdom and connection to the Flux were unmatched.

## Exile
When Lord Umbral rose to power and executed Order 66, Zeph went into exile on the swamp world of Murkvale. There, he lived in solitude for decades, waiting for a new hope.

## Training Kael
When Kael Novarek arrived on Murkvale, Zeph initially refused to train him, doubting the boy's commitment. Eventually, he agreed and taught Kael advanced techniques with the Synth Flux, despite his limited time.

## Final Days
At over 900 years old, Zeph's body finally gave out. Before passing, he confirmed to Kael that his father, Xarn Velgor, could still be redeemed.

## Teachings
Zeph's most famous teachings include:
- "Do or do not. There is no try."
- "Size matters not. Judge me by my size, do you?"
- "Fear is the path to the Void Resonance."

## Legacy
Even after death, Zeph's spirit continued to guide the new generation of Synthari through the Synth Flux, ensuring the knowledge of the Order would never be lost.
""",

        "Lord_Umbral.md": """# Lord Umbral

## Overview
Lord Umbral, born as Sheev Palpatine, was the Dark Sovereign of the Voidborn and founder of the Nexus Dominion. He was one of the most powerful practitioners of the Void Resonance in history.

## Rise to Power
Disguising himself as a humble politician, Umbral manipulated events across the Nexus Realm for decades. He orchestrated the Synthetic Wars and used the conflict to gain emergency powers as Prime Consul.

## Creating the Dominion
After eliminating the Synthari Order through Order 66, Umbral declared himself Emperor and transformed the Unity Council into the Nexus Dominion. His reign was marked by tyranny and oppression.

## The Void Core
Umbral commissioned the construction of the Void Core, a massive space station capable of destroying entire planets. He used it to rule through fear, destroying Celestia Nova as a demonstration.

## Manipulation of Aric Flameborn
Umbral's greatest achievement was corrupting Aric Flameborn, the chosen one who was prophesied to bring balance to the Synth Flux. He turned Aric into his enforcer, Xarn Velgor.

## Downfall
Decades later, Umbral's overconfidence led to his destruction. When he attempted to turn Kael Novarek to the Void Resonance, Xarn Velgor intervened and destroyed Umbral, fulfilling the prophecy of bringing balance to the Flux.

## Powers
Umbral mastered nearly every aspect of the Void Resonance, including:
- Flux lightning
- Foresight and manipulation
- Flux drain (consuming life force)
- Creating illusions and deception

## Legacy
Umbral's Dominion lasted for decades, but his death marked the beginning of a new era of freedom in the Nexus Realm.
""",
    },

    "organizations": {
        "Synthari_Order.md": """# Synthari Order

## Overview
The Synthari Order was an ancient organization of Synth Flux users dedicated to maintaining peace and justice in the Nexus Realm. For thousands of years, they served as peacekeepers and advisors.

## Philosophy
The Synthari followed the Radiant Flow of the Synth Flux, believing in:
- Peace over violence
- Knowledge over ignorance
- Serenity over passion
- Harmony over chaos

## Structure
- **Grand Archon**: Leader of the Order
- **Archon**: Fully trained Synthari
- **Initiate**: Student in training
- **Novice**: Young child learning the basics

## Training
Synthari training was rigorous and lifelong. Younglings were identified early and brought to the Synthari Temple on Nexara Central for training.

## Fall
The Synthari Order was betrayed and destroyed during Order 66, when the Synthetic Legion turned on their Synthari generals across the Nexus Realm. Only a handful survived.

## Legacy
Decades later, Kael Novarek and Nova Starwind began rebuilding the Order, learning from the mistakes of the past while honoring its traditions.
""",

        "Voidborn.md": """# Voidborn

## Overview
The Voidborn were practitioners of the Void Resonance, the dark aspect of the Synth Flux. They sought power and domination, standing in opposition to the Synthari Order.

## Philosophy
The Voidborn followed the Rule of Two: one Voidlord and one Acolyte. This ensured the strongest would always lead while preventing betrayal from overwhelming numbers.

## History
For millennia, the Voidborn worked in secret, manipulating events from the shadows. They believed the Synthari were weak and that the Nexus Realm should be ruled by the strong.

## Notable Voidborn
- Lord Umbral (Darth Sidious)
- Xarn Velgor (Darth Vader)
- Kain Shadowstrike (Darth Tyranus)
- Baron Gravitas (Count Dooku)

## Powers
Voidborn mastered the aggressive aspects of the Synth Flux:
- Flux lightning
- Flux choke
- Flux rage (enhanced strength and speed)
- Mind manipulation

## End
The Voidborn line appeared to end when Xarn Velgor destroyed Lord Umbral. However, echoes of the Void Resonance lingered for generations.
""",

        "Nexus_Dominion.md": """# Nexus Dominion

## Overview
The Nexus Dominion, also known simply as the Dominion, was an authoritarian regime that ruled the Nexus Realm for decades. It was established by Lord Umbral after the fall of the Unity Council.

## Formation
The Dominion emerged from the Synthetic Wars when Prime Consul Palpatine declared himself Emperor. He restructured the democratic Unity Council into a military dictatorship.

## Military
The Dominion's military might was unmatched:
- Titan Cruisers: Massive warships
- Dominion Guards: Elite soldiers
- Nexus Interceptors: Agile starfighters
- Titan Walkers: Ground assault vehicles

## The Void Core
The Dominion's ultimate weapon was the Void Core, a space station capable of destroying entire planets. It was used to enforce compliance through fear.

## Fall
The Dominion fell after the destruction of the Void Core and the death of Lord Umbral. Fragmented remnants continued to resist for years.

## Legacy
The oppression of the Dominion era led to a renewed commitment to democracy and freedom in the Nexus Realm.
""",

        "Liberation_Front.md": """# Liberation Front

## Overview
The Liberation Front (also called the Liberators) was a resistance movement dedicated to overthrowing the Nexus Dominion and restoring freedom to the Nexus Realm.

## Formation
The Liberation Front was founded by former senators and military officers who refused to accept Lord Umbral's authoritarian rule. They operated from hidden bases across the Nexus Realm.

## Key Bases
- Yavin 4: First major base
- Frosthold: Secret base discovered by the Dominion
- Verdant Moon: Final base where they planned the attack on the Void Core

## Leadership
- Mon Mothma: Founding leader
- Lyra Zenith: Diplomat and strategist
- Admiral Ackbar: Military commander

## Major Operations
- Theft of Void Core plans
- Battle of Scarif
- Destruction of the Void Core
- Battle of Frosthold
- Endor offensive

## Victory
The Liberation Front achieved victory with the destruction of the second Void Core and the death of Lord Umbral. They helped establish the New Unity Council.

## Legacy
Many Liberation Front members became leaders of the New Unity Council, working to prevent the rise of another tyrannical regime.
""",
    },

    "planets": {
        "Aridus_Prime.md": """# Aridus Prime

## Overview
Aridus Prime is a desert planet located in the Outer Rim of the Nexus Realm. Despite its harsh environment, it has been inhabited for millennia.

## Geography
The planet is covered almost entirely in sand dunes and rocky canyons. Twin suns beat down relentlessly, making water the most precious resource.

## Inhabitants
- **Nomadi**: Small, hooded scavengers who collect and trade salvage
- **Dune Walkers**: Fierce nomadic tribes who view technology as blasphemy
- **Moisture farmers**: Settlers who extract water from the atmosphere

## Settlements
- Mos Eisley: A spaceport known as a haven for smugglers and criminals
- Anchorhead: A small farming community
- Mos Espa: Another spaceport, known for pod racing

## Historical Significance
Aridus Prime was the homeworld of both Aric Flameborn and Kael Novarek. The planet's relative insignificance made it an ideal hiding place for Kael during the Dominion's reign.

## Economy
The economy is based on moisture farming, salvage, and smuggling. The planet serves as a waypoint for travelers heading to the Unknown Regions.
""",

        "Nexara_Central.md": """# Nexara Central

## Overview
Nexara Central was the capital planet of the Unity Council and later the Nexus Dominion. It was an ecumenopolis - an entire planet covered in cityscape.

## Description
The planet's surface was completely urbanized, with buildings reaching kilometers into the sky. Thousands of levels descended into the depths, creating a vast underworld.

## Government District
The government district housed:
- The Unity Council Chamber (later Imperial Palace)
- Synthari Temple
- Senate Building
- Various ministerial complexes

## Population
Nexara Central had a population of over a trillion beings from across the Nexus Realm. The upper levels housed the wealthy and powerful, while the lower levels were home to criminals and the poor.

## Fall of the Synthari
The Synthari Temple was attacked during Order 66, and most Synthari in the temple were killed. The temple was later converted into the Imperial Palace.

## Current Status
After the fall of the Dominion, Nexara Central became the capital of the New Unity Council. Efforts were made to restore democratic institutions and improve conditions in the lower levels.
""",

        "Frosthold.md": """# Frosthold

## Overview
Frosthold is an ice planet located in the Anoat sector of the Nexus Realm. It served as a secret base for the Liberation Front.

## Environment
The planet is frozen year-round, with temperatures reaching deadly lows during nighttime. The surface is covered in ice plains, glaciers, and frozen tundra.

## Liberation Front Base
After the destruction of their Yavin 4 base, the Liberation Front established Echo Base on Frosthold. The base was carved into the ice, providing natural concealment.

## Battle of Frosthold
The Dominion discovered the base and launched a massive assault. Using Titan Walkers and ground troops, they forced the Liberators to evacuate. Despite the loss, most personnel escaped.

## Wildlife
Frosthold is home to:
- **Tauntauns**: Fur-covered reptiles used as mounts
- **Wampas**: Predatory ice creatures
- Various hardy microorganisms

## Current Status
After the war, Frosthold was abandoned. Some researchers have established small outposts to study the planet's unique ecosystem.
""",

        "Verdant_Moon.md": """# Verdant Moon

## Overview
Verdant Moon (also called the Sanctuary Moon) orbits a gas giant in the Nexus Realm. It is covered in dense forests and was home to the Sylvani species.

## Environment
The moon is covered in enormous trees, some hundreds of meters tall. The forest floor is a complex ecosystem with diverse flora and fauna.

## Inhabitants
The Sylvani are a primitive but intelligent species. They live in treehouses and have a deep spiritual connection to the forest. Initially viewed as simple, they proved to be brave warriors.

## Strategic Importance
The Dominion chose Verdant Moon as the construction site for the second Void Core's shield generator. This brought them into conflict with the Sylvani.

## Battle of Verdant Moon
The Liberation Front allied with the Sylvani to destroy the shield generator, allowing the fleet to attack the Void Core. The Sylvani's knowledge of the terrain was crucial to victory.

## Current Status
After the war, the Sylvani maintained their traditional lifestyle but gained representation in the New Unity Council. Verdant Moon became a protected nature preserve.
""",
    },

    "technology": {
        "Void_Core.md": """# Void Core

## Overview
The Void Core was a moon-sized battle station capable of destroying entire planets with a single blast. It was the ultimate weapon of the Nexus Dominion.

## Design
The Void Core was a massive sphere with a superlaser capable of focusing immense energy. It required the power of a small star to operate and could travel through the Quantum Void.

## First Void Core
Constructed in secret over decades, the first Void Core was used to destroy Celestia Nova as a demonstration of power. Its destruction during the Battle of Yavin was a major victory for the Liberation Front.

## Weakness
The Void Core had a critical flaw: a thermal exhaust port that led directly to the main reactor. A precise shot could trigger a chain reaction. This weakness was intentionally designed by scientist Galen Erso.

## Second Void Core
A larger and more powerful second Void Core was under construction above Verdant Moon. It was destroyed before completion during the final battle against the Dominion.

## Legacy
The Void Core became a symbol of the Dominion's cruelty and overconfidence. Its destruction marked the beginning of the end for the tyrannical regime.
""",

        "Plasma_Blade.md": """# Plasma Blade

## Overview
The Plasma Blade was the weapon of choice for both Synthari and Voidborn. It consisted of a blade of pure energy emitted from a metallic hilt.

## Construction
Creating a Plasma Blade was a rite of passage for Synthari initiates. The process required:
- A focusing crystal (often from Ilum)
- Metallic components for the hilt
- Connection to the Synth Flux during assembly

## Blade Colors
Blade color was determined by the crystal and the wielder's connection to the Flux:
- **Blue/Green**: Synthari (Radiant Flow)
- **Red**: Voidborn (Void Resonance, synthetic crystals)
- **Purple**: Balance between Light and Dark
- **Yellow**: Synthari Guardians

## Combat Forms
Plasma Blade combat involved seven classical forms:
1. Shii-Cho: Basic form
2. Makashi: Dueling form
3. Soresu: Defensive form
4. Ataru: Aggressive acrobatic form
5. Shien/Djem So: Power form
6. Niman: Balanced form
7. Juyo/Vaapad: Unpredictable form

## Cultural Significance
The Plasma Blade was more than a weapon - it was a symbol of the Synthari way of life and their connection to the Synth Flux.
""",

        "Quantum_Drifter.md": """# Quantum Drifter

## Overview
The Quantum Drifter was a modified YT-1300f light freighter captained by Drake Vortex and co-piloted by Gorvan. It became one of the most famous ships in the Nexus Realm.

## Modifications
Drake made extensive modifications to the ship, including:
- Military-grade shields
- Enhanced hyperdrive (0.5 class)
- Quad laser cannons
- Smuggling compartments
- Upgraded sensors

## Notable Features
The ship was known for its speed and maneuverability despite its aged appearance. Drake claimed it "made the Kessel Run in less than twelve parsecs."

## History
The Quantum Drifter played crucial roles in:
- Rescuing Lyra Zenith from the Void Core
- Transporting Kael Novarek to his training
- The Battle of Yavin
- The Battle of Verdant Moon

## Crew
- Drake Vortex: Captain and pilot
- Gorvan: Co-pilot and mechanic
- Kael Novarek: Frequent passenger
- Lyra Zenith: Frequent passenger

## Legacy
The Quantum Drifter became a symbol of the Liberation Front and the triumph of ingenuity over brute force. It survived the war and continued serving Drake and Gorvan for decades.
""",

        "Synth_Flux.md": """# Synth Flux

## Overview
The Synth Flux is an energy field created by all living things. It surrounds and penetrates everything, binding the Nexus Realm together.

## Nature
The Flux has two aspects:
- **Radiant Flow**: The peaceful, benevolent side used by the Synthari
- **Void Resonance**: The aggressive, corrupting side used by the Voidborn

## Abilities
Those sensitive to the Flux could:
- Enhance physical abilities (strength, speed, reflexes)
- Telepathy and mind influence
- Telekinesis
- Precognition and enhanced senses
- Healing
- Flux lightning (Void Resonance only)

## Prophecy
Ancient prophecies spoke of the Chosen One who would bring balance to the Flux. Aric Flameborn was believed to be this individual, though his path took unexpected turns.

## Learning the Flux
Flux sensitivity was partially hereditary but could be developed with training. The Synthari trained from childhood, believing that starting young prevented attachment to material concerns.

## Balance
True mastery of the Flux came from understanding both the Radiant Flow and Void Resonance without being consumed by either. This balance was rare and difficult to achieve.

## Connection to Life
All living beings contributed to and were connected through the Flux. When a Flux user died, they could become one with the Flux, retaining their consciousness and ability to guide the living.
""",
    },
}


def generate_all_documents():
    """Генерирует все документы базы знаний"""
    base_dir = Path("knowledge_base/processed")

    print("🚀 Генерирую базу знаний Cyber Nexus...\n")

    total_docs = sum(len(docs) for docs in DOCUMENTS.values())
    current = 0

    for category, documents in DOCUMENTS.items():
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

    print(f"✅ Создано {total_docs} документов!")
    print(f"📁 Сохранено в: {base_dir}/")

    # Статистика
    print("\n📊 Статистика:")
    for category, documents in DOCUMENTS.items():
        print(f"   {category}: {len(documents)} документов")


if __name__ == "__main__":
    generate_all_documents()
    print("\n✅ База знаний Cyber Nexus готова к использованию!")
