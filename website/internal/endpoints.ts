import jwt from "jsonwebtoken";
import {Endpoint, DefaultClient} from "rickety";

import {IGameResult, IGameSubmit, IGameToken, IDeck} from "./types";

class DelayClient extends DefaultClient {
    async send(request: any): Promise<any> {
        await new Promise((r) => setTimeout(r, 500));
        return super.send(request);
    }
}

class CreateGameClient extends DelayClient {
    async send(request: any): Promise<any> {
        // TODO type checks
        const {deck} = JSON.parse(request.body);
        request.url += `/game?deck=${deck}`;
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

export const CreateGame = new Endpoint<{deck: IDeck}, IGameToken>({
    client: new CreateGameClient(),
    method: "GET",
    path: "/api",
});

class SubmitGameClient extends DelayClient {
    async send(request: any): Promise<any> {
        // TODO type checks
        const body = JSON.parse(request.body);
        body.token = body.token.raw;
        request.url += `/submit`
        return super.send(
            Object.assign({}, request, {
                body: JSON.stringify(body),
            }),
        );
    }
}

export const SubmitGame = new Endpoint<IGameSubmit, IGameResult>({
    client: new SubmitGameClient(),
    path: "/api",
});
