import {Endpoint, DefaultClient} from "rickety";
import {Game} from "./types";

const client = new DefaultClient();

export const createGame = new Endpoint<{}, Game>({
    client,
    path: "/game",
});
