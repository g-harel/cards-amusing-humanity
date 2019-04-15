import jwt from "jsonwebtoken";
import {Endpoint, DefaultClient} from "rickety";

import {IGameResult, IGameSubmit, IGameToken, Extension} from "./types";

class DelayClient extends DefaultClient {
    async send(request: any): Promise<any> {
        await new Promise((r) => setTimeout(r, 500));
        return super.send(request);
    }
}

class CreateGameClient extends DelayClient {
    async send(request: any): Promise<any> {
        // TODO type checks
        const {extension} = JSON.parse(request.body);
        request.url += `?extension=${extension}`;
        request.body = undefined;
        const response = await super.send(request);
        const token = JSON.parse(response.body).token;
        const payload = jwt.decode(token) || {};
        (payload as any).raw = token;
        return Object.assign({}, response, {
            body: JSON.stringify(payload),
        });
    }
}

export const CreateGame = new Endpoint<{extension: Extension}, IGameToken>({
    client: new CreateGameClient(),
    method: "GET",
    path: "/game",
});

class SubmitGameClient extends DelayClient {
    async send(request: any): Promise<any> {
        // TODO type checks
        const body = JSON.parse(request.body);
        body.token = body.token.raw;
        return super.send(
            Object.assign({}, request, {
                body: JSON.stringify(body),
            }),
        );
    }
}

export const SubmitGame = new Endpoint<IGameSubmit, IGameResult>({
    client: new SubmitGameClient(),
    path: "/submit",
});
