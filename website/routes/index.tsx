import { BlockedUser } from "../src/mod.ts";
import { Handlers, PageProps } from "$fresh/server.ts";
import { fetchBlockList } from "../src/mod.ts";
import BlockListTable from "../components/BlockListTable.tsx";

export const handler: Handlers<BlockedUser[]> = {
  GET: async (_req, ctx) => {
    const blockedUsers = await fetchBlockList();
    return ctx.render(blockedUsers);
  },
};

export default function Home(props: PageProps<BlockedUser[]>) {
  const blockedUsers = props.data;
  return (
    <div class="min-w-[60%] max-w-[80%] m-auto pb-10">
      <div class="flex children:mx-3 m-auto justify-center py-10 pb-0">
        <img
          src="/pals.png"
          alt="Spelltable Pals"
          class="w-24 h-24 rounded-md"
        />
        <div class="children:text-left">
          <h1 class="font-bold text-6xl">Spelltable Pals</h1>
            <a href="/discord" target="_blank" class="underline text-2xl">
            Join our Discord!
            </a>
        </div>
      </div>
      <div class="m-auto p-4 w-[50%] children:py-1">
            <h2 class="text-3xl italic text-center">Caution List</h2>
        <p>
          The List names users that Spelltable Pals have had negative
          experiences with, to varying degrees.
        </p>
        <p>
          If you are a Spelltable Pals member, you may refer to The List when
          joining games to see if another player has been flagged by the
          community for bigotry, aggression, misrepresenting their deck, etc.
          You can also download the Chrome extension{" "}
          <a
            class="text-blue-600 underline"
            target="_blank"
            href="https://github.com/ItsGoldeneyes/SpelltablePals"
          >
            here
          </a>.
        </p>
        <p>
          If you are not a Spelltable Pals member & your name is listed, you may
          contact us to discuss the circumstances surrounding your caution.
        </p>
        <p>
          Keep Magic the Gathering Fun!
        </p>
      </div>
      <div class="flex-row justify-center items-center">
        <BlockListTable
          blocked_users={blockedUsers}
          class="m-auto children:(children:(first:(bg-[rgba(0,0,0,0.5)] text-white) even:(bg-[rgba(0,0,0,0.2)]) p-3) border border-gray-300)"
        />
      </div>
    </div>
  );
}
