import jwt from "jsonwebtoken";
import {Endpoint} from "rickety";

import {IGameResult, IGameSubmit, IGameToken} from "./types";

export const CreateGame = new Endpoint<{}, IGameToken>({
    client: {
        send: async () => {
            await new Promise((r) => setTimeout(r, 400));
            const res: IGameToken = {
                raw: "",
                question: {
                    id: "b1",
                    description: "What gets better with age?",
                },
                answers: [
                    {id: "w1", description: "Daddy's credit card."},
                    {id: "w2", description: "Drinking alone."},
                    {id: "w3", description: "The glass ceiling."},
                    {id: "w4", description: "A lifetime of sadness."},
                    {id: "w5", description: "A PowerPoint presentation."},
                ],
            };
            res.raw = jwt.sign(res, "-");
            return {status: 200, body: JSON.stringify(res)};
        },
    },
    method: "GET",
    path: "/game",
});

export const SubmitGame = new Endpoint<IGameSubmit, IGameResult>({
    client: {
        send: async () => {
            await new Promise((r) => setTimeout(r, 400));
            const res: IGameResult = {similarity: 42.314};
            return {status: 200, body: JSON.stringify(res)};
        },
    },
    path: "/submit",
});
