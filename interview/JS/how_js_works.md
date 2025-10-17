# How JavaScript runs: Browser vs Node.js

Here’s a clear, step‑by‑step overview of what happens when JavaScript runs in the browser and in Node.js, plus the key components in each environment. I’ll keep it practical and then we’ll do a quick self‑check.

## Big picture
- Both environments use a JS engine (like V8) that parses, compiles, and executes your code.
- Both use an event loop with task queues so async work doesn’t block the main thread.
- The main differences are the surrounding platform: browser Web APIs vs Node’s libuv and native bindings.

***

## In the Browser: step‑by‑step flow
1) Load & parse
- HTML is parsed; <script> tags are fetched and their JS source is given to the engine.
- The engine tokenizes and parses JS to an AST, then produces bytecode for the interpreter and may optimize hot code later.

2) Execute synchronous code
- The engine runs your top‑level code on the call stack until it completes. No event loop work happens until the stack is empty.

3) Delegate async work to Web APIs
- Calls like setTimeout, fetch, addEventListener, MutationObserver are handed to the browser’s Web APIs.
- These run outside the JS engine and signal completion later.

4) Queue callbacks
- When async work finishes, callbacks are queued:
  - Microtask queue: Promise reactions, queueMicrotask, MutationObserver.
  - Macrotask (task) queue: timers, UI events, message events, etc.

5) Event loop turn
- After the call stack empties, the event loop drains all microtasks before taking the next macrotask. This is why Promise.then often runs before setTimeout.

6) Render
- Between macrotasks (and after microtasks), the browser may perform layout/paint, then proceed to the next task.

Browser components
- JS Engine (e.g., V8): Parser, Interpreter (Ignition), Optimizing compiler (TurboFan), Garbage collector.
- Web APIs: timers, DOM, fetch/XHR, canvas, storage, etc.
- Task queues: microtask queue, macrotask (task) queue.
- Event loop: coordinates stack/queues and rendering.

Notes
- Promises and queueMicrotask schedule microtasks (higher priority than macrotasks).[1][2]
- The event loop executes tasks, drains microtasks, and hands back control to rendering.[3][2][1]

***

## In Node.js: step‑by‑step flow
1) Load & parse
- Node starts V8, which parses your script to AST, generates bytecode, runs in the interpreter, and optimizes hot code.

2) Execute synchronous code
- Top‑level code runs to completion on the main thread’s call stack.

3) Delegate async work via native bindings
- Operations like fs, crypto, DNS, and some networking calls go through Node’s C++ bindings to libuv.
- libuv uses the OS (and a thread pool when needed) to perform I/O off the main thread.

4) Queue callbacks into event‑loop phases
- libuv signals completion; callbacks are queued in event loop phases (timers, pending callbacks, idle/prepare, poll, check, close callbacks).
- Microtasks also exist in Node (Promise reactions/queueMicrotask) and are processed between ticks and after each phase.

5) Event loop iteration
- Each tick processes a phase in order, executes ready callbacks, then drains microtasks, then advances to the next phase.

6) Process exits when work is done
- When there are no more handles/timers or pending tasks, the process ends.

Node.js components
- V8 engine: Parser, Ignition, TurboFan, GC.
- Node C++ bindings: bridge between JS and native subsystems.
- libuv: event loop, I/O polling, thread pool, timer management.
- Event loop phases: timers → pending callbacks → idle/prepare → poll → check (setImmediate) → close callbacks.
- Task queues: microtask queue (Promises), macrotask queues per phase; process.nextTick queue (runs before other microtasks in Node).

Notes
- libuv is a library powering Node’s event loop and async I/O; it’s not the JS engine itself.[4][5]
- Promise microtasks and queueMicrotask run with high priority; Node also has process.nextTick which runs even before microtasks in many cases.[6][5]

***

## Key differences: quick compare
- Platform APIs: Browser Web APIs (DOM, fetch) vs Node core modules + libuv (fs, net, crypto).
- Rendering: Browsers interleave rendering; Node has no rendering step.
- Event loop details: Browsers focus on microtask vs task; Node exposes distinct libuv phases and process.nextTick.
- Security/runtime: Browsers sandbox and expose DOM; Node exposes filesystem and OS resources.

***

## Mini‑check (your turn)
- Q1: In the browser, which runs first after the call stack empties: a Promise.then callback or a setTimeout callback? Why?
- Q2: In Node, name two responsibilities of libuv.
- Q3: When does the browser typically render relative to tasks and microtasks?

If you’d like, tell me your target depth (e.g., interview‑prep vs internals) and I’ll tailor with diagrams, code demos, or tricky edge cases.

[1](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide)
[2](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide/In_depth)
[3](https://javascript.info/event-loop)
[4](https://dev.to/_staticvoid/node-js-under-the-hood-3-deep-dive-into-the-event-loop-135d)
[5](https://www.builder.io/blog/visual-guide-to-nodejs-event-loop)
[6](https://www.red-gate.com/simple-talk/development/javascript/microtask-queues-in-node-js-event-loop/)
[7](https://www.youtube.com/watch?v=eiC58R16hb8)
[8](https://dev.to/bymarsel/unraveling-macrotasks-and-microtasks-in-javascript-what-every-developer-should-know-53mc)
[9](https://stackoverflow.com/questions/54957946/what-does-v8s-ignition-really-do)
[10](https://www.linkedin.com/pulse/event-loop-heart-javascript-hari-mohan-prajapat-3kbwc)
[11](https://blog.bitsrc.io/you-dont-know-node-js-eventloop-8ee16831767)
[12](https://benediktmeurer.de/2016/11/25/v8-behind-the-scenes-november-edition/)
[13](https://en.wikipedia.org/wiki/V8_(JavaScript_engine))
[14](https://javascript.plainenglish.io/event-loop-explained-unlocking-javascripts-core-engine-9f2a5466d875)
[15](https://www.thenodebook.com/node-arch/event-loop-intro)
[16](https://dev.to/_staticvoid/node-js-under-the-hood-7-the-new-v8-4gd6)
[17](https://www.zartis.com/nodejs-threads-and-the-event-loop/)
[18](https://leapcell.io/blog/javascript-core-and-v8-a-deep-dive-into-engine-architecture-and-performance)
[19](https://exploringjs.com/nodejs-shell-scripting/ch_nodejs-overview.html)
[20](https://v8.dev/blog/launching-ignition-and-turbofan)