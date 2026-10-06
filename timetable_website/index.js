(function() {
            // -------------------------------------------------------------
            // 1. DATA – edit this
            //    Times are "HH:MM"
            //    Slots are generated from DAY_START to DAY_END in SLOT_MINUTES steps
            // -------------------------------------------------------------
            const scheduleData = {
                days: [
                    {
                        name: 'Monday',
                        sessions: [
                            {
                                id: 'microcontroller-programming-lecture',
                                type: 'lecture',
                                title: 'Programování mikrokontrolerů',
                                start: '09:00',
                                end: '10:30',           
                                links: {
                                    classPage: 'https://ktiml.mff.cuni.cz/~obdrzalek/vyuka/NPRG037/',
                                    ATMega328PBDatasheet: 'https://ww1.microchip.com/downloads/en/DeviceDoc/40001906A.pdf',
                                    AVRInstructionSet: 'https://ww1.microchip.com/downloads/en/DeviceDoc/AVR-InstructionSet-Manual-DS40002198.pdf'
                                },
                                tags: [],
                                note: 'Pry je dobre, aby si mne z prednasky pamatoval, nema rad lidi, co chteji jen kredity'
                            },
                            {
                                id: 'microcontroller-programming-practical',
                                type: 'practical',
                                title: 'Programování mikrokontrolerů',
                                start: '10:40',
                                end: '12:10',           
                                links: {
                                    classPage: 'https://ktiml.mff.cuni.cz/~obdrzalek/vyuka/NPRG037/cviceni.html',
                                    ATMega328PBDatasheet: 'https://ww1.microchip.com/downloads/en/DeviceDoc/40001906A.pdf',
                                    AVRInstructionSet: 'https://ww1.microchip.com/downloads/en/DeviceDoc/AVR-InstructionSet-Manual-DS40002198.pdf'
                                },
                                tags: [],
                                note: ''
                            },
                            {
                                id: 'error-correcting-codes-lecture',
                                type: 'lecture',
                                title: 'Samoopravné kódy',
                                start: '12:20',
                                end: '13:50',          
                                links: {
                                    classPage: 'https://www.karlin.mff.cuni.cz/~zemlicka/26-27/vyuka.htm',
                                    scripts: 'https://www.karlin.mff.cuni.cz/~zemlicka/26-27/SoKn.pdf'
                                },
                                tags: ['optional'],
                                note: ''
                            },
                            {
                                id: 'program-semantics',
                                type: 'practical',
                                title: 'Sémantika programů ',
                                start: '12:20',
                                end: '13:50',           
                                links: {
                                  classPage: 'https://d3s.mff.cuni.cz/cz/teaching/nswi183/'
                                },
                                tags: ['priority'],
                                note: ''
                            },
                            {
                                id: 'cpp-programming-practical',
                                type: 'practical',
                                title: 'Programování v C++ ',
                                start: '14:00',
                                end: '15:30',           
                                links: {
                                    classPage: 'https://teaching.mff.cuni.cz/nprg041-web/',
                                    recodex: 'https://recodex.mff.cuni.cz/',
                                    wiki: 'https://wiki.matfyz.cz/NPRG041'
                                },
                                tags: ['priority'],
                                note: ''
                            }
                        ]
                    },
                    {
                        name: 'Tuesday',
                        sessions: [
                           {
                                id: 'error-correcting-codes-practical',
                                type: 'practical',
                                title: 'Samoopravné kódy',
                                start: '17:20',
                                end: '18:50',          
                                links: {
                                    classPage: 'https://www.karlin.mff.cuni.cz/~zemlicka/26-27/vyuka.htm',
                                    scripts: 'https://www.karlin.mff.cuni.cz/~zemlicka/26-27/SoKn.pdf'
                                },
                                tags: ['optional'],
                                note: ''
                            },
                            {
                                id: 'java-programming-practical',
                                type: 'practical',
                                title: 'Programování v jazyce Java',
                                start: '12:20',
                                end: '13:50',           
                                links: {
                                    classPage: 'https://d3s.mff.cuni.cz/teaching/nprg013/',
                                    recodex: 'https://recodex.mff.cuni.cz/',
                                    wiki: 'https://wiki.matfyz.cz/NPRG013'
                                },
                                tags: [],
                                note: ''
                            }
                        ]
                    },
                    {
                        name: 'Wednesday',
                        sessions: [
                            {
                                id: 'java-programming-lecture',
                                type: 'lecture',
                                title: 'Programování v jazyce Java',
                                start: '09:00',
                                end: '10:30',           
                                links: {
                                    classPage: 'https://d3s.mff.cuni.cz/teaching/nprg013/',
                                    recodex: 'https://recodex.mff.cuni.cz/',
                                    wiki: 'https://wiki.matfyz.cz/NPRG013'
                                },
                                tags: [],
                                note: ''
                            },
                            {
                                id: 'cpp-programming-lecture',
                                type: 'lecture',
                                title: 'Programování v C++',
                                start: '12:20',
                                end: '13:50',           
                                links: {
                                    classPage: 'https://teaching.mff.cuni.cz/nprg041-web/',
                                    recodex: 'https://recodex.mff.cuni.cz/',
                                    wiki: 'https://wiki.matfyz.cz/NPRG041'
                                },
                                tags: ['priority'],
                                note: ''
                            },
                            {
                                id: 'mathematical-analysis-practical',
                                type: 'practical',
                                title: 'Matematická analýza 2',
                                start: '15:40',
                                end: '17:10',           
                                links: {
                                    classPage: 'https://is.cuni.cz/studium/predmety/index.php?id=8dd0533e31ad2ba1aff2bfbcf9f399ac&tid=&do=predmet&kod=NMAI055&skr=2026&fak=11320',
                                    wiki: 'https://wiki.matfyz.cz/NMAI055'
                                },
                                tags: [],
                                note: ''
                            }
                        ]
                    },
                    {
                        name: 'Thursday',
                        sessions: [
                            {
                                id: 'mathematical-analysis-lecture',
                                type: 'lecture',
                                title: 'Matematická analýza 2',
                                start: '09:00',
                                end: '10:30',           
                                links: {
                                  classPage: 'https://kam.mff.cuni.cz/~klazar/MAII26cz.html',
                                  wiki: 'https://wiki.matfyz.cz/NMAI055'
                                },
                                tags: [],
                                note: ''
                            },
                            {
                                id: 'compiler-principles-lecture',
                                type: 'lecture',
                                title: 'Principy překladačů',
                                start: '12:20',
                                end: '13:50',           
                                links: {
                                    classPage: 'https://teaching.mff.cuni.cz/nswi098-web/',
                                    wiki: 'https://wiki.matfyz.cz/NSWI098'
                                },
                                tags: [],
                                note: ''
                            },
                            {
                                id: 'compiler-principles-practical',
                                type: 'practical',
                                title: 'Principy překladačů',
                                start: '14:00',
                                end: '15:30',           
                                links: {
                                    classPage: 'https://teaching.mff.cuni.cz/nswi098-web/',
                                    wiki: 'https://wiki.matfyz.cz/NSWI098'
                                },
                                tags: [],
                                note: ''
                            }                            
                        ]
                    },
                    {
                        name: 'Friday',
                        sessions: []
                    }
                ]
            };

            // -------------------------------------------------------------
            // 2. Link metadata (icon + label)
            // -------------------------------------------------------------
            const linkMeta = {
                classPage: { icon: '', label: 'Class page' },
                recodex: { icon: '', label: 'Recodex' },
                owl: { icon: '', label: 'Owl' },
                wiki: { icon: '', label: 'Wiki page' },
                additional: { icon: '', label: 'Additional' },
                scripts: {icon: '', label: 'Skripta'}
            };

            function getLinkMeta(key) {
                if (linkMeta[key]) return linkMeta[key];
                const friendly = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
                return { icon: '', label: friendly };
            }

            // -------------------------------------------------------------
            // 3. Time configuration
            // -------------------------------------------------------------
            const DAY_START = '07:20';
            const DAY_END = '19:50';
            const SLOT_MINUTES = 30;

            // convert "HH:MM" → minutes
            function timeToMinutes(t) {
                const [h, m] = t.split(':').map(Number);
                return h * 60 + m;
            }

            function minutesToTime(min) {
                const h = Math.floor(min / 60);
                const m = min % 60;
                return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
            }

            const dayStartMin = timeToMinutes(DAY_START);
            const dayEndMin = timeToMinutes(DAY_END);

            // build list of slot start minutes
            const timeSlots = [];
            for (let t = dayStartMin; t < dayEndMin; t += SLOT_MINUTES) {
                timeSlots.push(t);
            }

            // The pixel height of one slot (30 min) — we set this once and use it
            // for positioning. The total timetable height = timeSlots.length * SLOT_HEIGHT.
            const SLOT_HEIGHT = 40; // px per 30-minute slot

            // total body height:
            const BODY_HEIGHT = timeSlots.length * SLOT_HEIGHT;

            // -------------------------------------------------------------
            // 4. Pre-process sessions
            //    We need, for each day, a list of sessions with:
            //    - top offset in px
            //    - height in px
            //    - overlap grouping (side-by-side)
            // -------------------------------------------------------------
            const dayNames = scheduleData.days.map(d => d.name);
            const daySessions = scheduleData.days.map(day => {
                return day.sessions.map(session => {
                    const startMin = timeToMinutes(session.start);
                    const endMin = timeToMinutes(session.end);
                    const top = ((startMin - dayStartMin) / SLOT_MINUTES) * SLOT_HEIGHT;
                    const height = ((endMin - startMin) / SLOT_MINUTES) * SLOT_HEIGHT;
                    return { session, startMin, endMin, top, height };
                });
            });

            // Assign overlap columns: for each day, find overlapping groups
            // and split them horizontally.
            daySessions.forEach(sessions => {
                // sort by start time
                sessions.sort((a, b) => a.startMin - b.startMin || a.endMin - b.endMin);

                // We'll mark each session with overlapIndex and overlapCount
                // Simple approach: for each session, find all others that overlap it.
                // This handles up to a few overlaps nicely.
                sessions.forEach((s, i) => {
                    const overlapping = sessions.filter(o =>
                        o.startMin < s.endMin && o.endMin > s.startMin
                    );
                    // remove self
                    const others = overlapping.filter(o => o !== s);
                    // find index of s within overlapping (sorted by start)
                    const sortedOverlapping = [...overlapping].sort(
                        (a, b) => a.startMin - b.startMin || a.endMin - b.endMin
                    );
                    s.overlapIndex = sortedOverlapping.indexOf(s);
                    s.overlapCount = sortedOverlapping.length;
                });
            });

            // -------------------------------------------------------------
            // 5. Render header
            // -------------------------------------------------------------
            const ttHeader = document.getElementById('ttHeader');
            const ttBody = document.getElementById('ttBody');

            function renderHeader() {
                ttHeader.innerHTML = '';
                const corner = document.createElement('div');
                corner.className = 'tt-corner';
                corner.textContent = '';
                ttHeader.appendChild(corner);

                dayNames.forEach(dayName => {
                    const dayCol = document.createElement('div');
                    dayCol.className = 'tt-day-header';
                    dayCol.textContent = dayName;
                    ttHeader.appendChild(dayCol);
                });
            }

            // -------------------------------------------------------------
            // 6. Render body
            // -------------------------------------------------------------
            function renderBody() {
                ttBody.innerHTML = '';

                // We create a container for the rows, but since we're absolutely
                // positioning class blocks inside day cells, we need a structure
                // where each day cell spans the full height.

                // We'll create one row per time slot, and inside each day cell
                // we'll place the absolutely positioned class blocks.
                // But absolutely positioned elements need a positioned ancestor
                // that covers the full height. So instead, we'll structure it as:

                // .tt-body (position: relative)
                //   .tt-row (one per slot, position: relative)
                //     .tt-time (left column)
                //     .tt-day-cell (position: relative, height: SLOT_HEIGHT)
                //       ... but this would clip blocks that span multiple slots.

                // Better: create a single "body grid" with time column and day
                // columns, where each day column is a single tall cell, and
                // class blocks are absolutely positioned inside.

                // Let's restructure the DOM:
                // .tt-body
                //   .tt-body-grid (display: flex, height: BODY_HEIGHT)
                //     .tt-time-column (width 70px, contains one label per slot)
                //     .tt-day-column * 5 (position: relative, height: BODY_HEIGHT)
                //       .class-block (absolute, top/height)

                // This gives us full control and blocks can span slots.

                const grid = document.createElement('div');
                grid.className = 'tt-body-grid';
                grid.style.display = 'flex';
                grid.style.height = BODY_HEIGHT + 'px';
                grid.style.position = 'relative';

                // ---- time column ----
                const timeCol = document.createElement('div');
                timeCol.className = 'tt-time-column';
                timeCol.style.width = '70px';
                timeCol.style.minWidth = '70px';
                timeCol.style.flexShrink = '0';
                timeCol.style.borderRight = '1px solid #c9d9e8';
                timeCol.style.background = '#f6faff';
                timeCol.style.position = 'relative';

                timeSlots.forEach((slotMin, idx) => {
                    const timeCell = document.createElement('div');
                    timeCell.className = 'tt-time';
                    timeCell.style.height = SLOT_HEIGHT + 'px';
                    timeCell.style.boxSizing = 'border-box';
                    timeCell.style.borderBottom = '1px solid #d6e2ed';
                    timeCell.textContent = minutesToTime(slotMin);
                    timeCell.style.display = 'flex';
                    timeCell.style.alignItems = 'flex-start';
                    timeCell.style.justifyContent = 'flex-end';
                    timeCell.style.padding = '0.15rem 0.3rem 0 0.3rem';
                    timeCell.style.fontSize = '0.65rem';
                    timeCell.style.fontWeight = '500';
                    timeCell.style.color = '#2c577a';
                    timeCol.appendChild(timeCell);
                });

                grid.appendChild(timeCol);

                // ---- day columns ----
                dayNames.forEach((dayName, dayIdx) => {
                    const dayCol = document.createElement('div');
                    dayCol.className = 'tt-day-column';
                    dayCol.style.flex = '1';
                    dayCol.style.minWidth = '120px';
                    dayCol.style.borderRight = '1px solid #e2edf6';
                    dayCol.style.position = 'relative';
                    dayCol.style.background = '#ffffff';

                    // draw horizontal grid lines (slot separators)
                    timeSlots.forEach((_, idx) => {
                        const line = document.createElement('div');
                        line.style.position = 'absolute';
                        line.style.left = '0';
                        line.style.right = '0';
                        line.style.top = ((idx + 1) * SLOT_HEIGHT) + 'px';
                        line.style.height = '1px';
                        line.style.background = '#e8eef5';
                        line.style.pointerEvents = 'none';
                        dayCol.appendChild(line);
                    });

                    // place class blocks
                    const sessions = daySessions[dayIdx] || [];
                    sessions.forEach(item => {
                        const { session, top, height, overlapIndex, overlapCount } = item;

                        const block = document.createElement('div');
                        block.className = `class-block ${session.type}`;
                        block.dataset.sessionId = session.id;

                        // position
                        block.style.top = top + 'px';
                        block.style.height = height + 'px';

                        // horizontal overlap handling
                        if (overlapCount > 1) {
                            const widthPercent = 100 / overlapCount;
                            const leftPercent = overlapIndex * widthPercent;
                            block.style.left = `calc(${leftPercent}% + 0.2rem)`;
                            block.style.right = `calc(${100 - (leftPercent + widthPercent)}% + 0.2rem)`;
                        } else {
                            block.style.left = '0.2rem';
                            block.style.right = '0.2rem';
                        }

                        // content
                        const title = document.createElement('div');
                        title.className = 'cb-title';
                        title.textContent = session.title;

                        const meta = document.createElement('div');
                        meta.className = 'cb-meta';
                        const timeSpan = document.createElement('span');
                        timeSpan.textContent = `${session.start}–${session.end}`;
                        meta.appendChild(timeSpan);

                        block.appendChild(title);
                        block.appendChild(meta);

                        block.addEventListener('click', (e) => {
                            e.stopPropagation();
                            openLinksForSession(session.id);
                        });

                        dayCol.appendChild(block);
                    });

                    grid.appendChild(dayCol);
                });

                ttBody.appendChild(grid);
            }

            // -------------------------------------------------------------
            // 7. Drawer logic
            // -------------------------------------------------------------
            const drawerPlaceholder = document.getElementById('drawerPlaceholder');
            const drawerContent = document.getElementById('drawerContent');
            const drawerClassTitle = document.getElementById('drawerClassTitle');
            const drawerClassMeta = document.getElementById('drawerClassMeta');
            const drawerLinkList = document.getElementById('drawerLinkList');
            const drawerNote = document.getElementById('drawerNote');

            // Build a lookup: sessionId -> { session, dayName }
            const sessionLookup = new Map();
            scheduleData.days.forEach(day => {
                day.sessions.forEach(session => {
                    sessionLookup.set(session.id, { session, dayName: day.name });
                });
            });

            function openLinksForSession(sessionId) {
                const entry = sessionLookup.get(sessionId);
                if (!entry) return;
                const { session, dayName } = entry;

                // header
                drawerClassTitle.textContent = session.title;

                // meta: day, time, type
                drawerClassMeta.innerHTML = '';
                const daySpan = document.createElement('span');
                daySpan.textContent = dayName;
                const timeSpan = document.createElement('span');
                timeSpan.textContent = `${session.start}–${session.end}`;
                const typeSpan = document.createElement('span');
                typeSpan.textContent = session.type === 'lecture' ? 'Lecture' : 'Practical';
                
                drawerClassMeta.appendChild(daySpan);
                drawerClassMeta.appendChild(timeSpan);
                drawerClassMeta.appendChild(typeSpan);

                if (session.tags) {
                    for (const tag of session.tags) {
                        const tagSpan = document.createElement('span');
                        if (tag === 'priority') {
                            tagSpan.textContent = 'Priority';
                            tagSpan.classList.add('tag-priority');
                        } else if (tag === 'optional') {
                            tagSpan.textContent = 'Optional';
                            tagSpan.classList.add('tag-optional');
                        } else {
                            tagSpan.textContent = tag;
                        }
                        drawerClassMeta.appendChild(tagSpan);
                    }
                }

                // links
                drawerLinkList.innerHTML = '';
                const links = session.links || {};
                const validEntries = Object.entries(links).filter(([_, url]) => url && url.trim() !== '');

                if (validEntries.length === 0) {
                    const emptyMsg = document.createElement('div');
                    emptyMsg.className = 'no-links';
                    emptyMsg.textContent = 'No links provided for this class';
                    drawerLinkList.appendChild(emptyMsg);
                } else {
                    validEntries.forEach(([key, url]) => {
                        const meta = getLinkMeta(key);
                        const linkEl = document.createElement('a');
                        linkEl.className = 'link-item';
                        linkEl.href = url;
                        linkEl.target = '_blank';
                        linkEl.rel = 'noopener noreferrer';

                        const iconSpan = document.createElement('span');
                        iconSpan.className = 'link-icon';
                        iconSpan.textContent = meta.icon;

                        const labelSpan = document.createElement('span');
                        labelSpan.className = 'link-label';
                        labelSpan.textContent = meta.label;

                        linkEl.appendChild(iconSpan);
                        linkEl.appendChild(labelSpan);
                        linkEl.title = `${meta.label} (${key})`;

                        drawerLinkList.appendChild(linkEl);
                    });
                }

                drawerPlaceholder.style.display = 'none';
                drawerNote.style.display = 'none';
                drawerContent.style.display = 'block';

                if (window.innerWidth <= 800) {
                    document.getElementById('drawer').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }

                
                if (session.note && session.note.length > 0) {
                    const noteContainer = document.createElement("p");
                    noteContainer.innerHTML = `<b>Note:</b> ${session.note}`;
                    drawerNote.innerHTML = '';
                    drawerNote.appendChild(noteContainer);
                    drawerNote.style.display = 'block';
                }
            }

            // -------------------------------------------------------------
            // 8. Initialize
            // -------------------------------------------------------------
            renderHeader();
            renderBody();

            // optional test: open first session
            // openLinksForSession('mon-lecture-1');
        })();
