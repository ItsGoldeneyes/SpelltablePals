#!/usr/bin/env -S deno run -A --watch=static/,routes/

import dev from "$fresh/dev.ts";
import config from "./fresh.config.ts";

// deno-lint-ignore no-external-import
// import "https://deno.land/x/twindellisense@v1.0.0/load.ts";

await dev(import.meta.url, "./main.ts", config);
