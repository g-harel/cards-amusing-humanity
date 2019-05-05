import jwt from "jsonwebtoken";
import {Endpoint} from "rickety";
import {ClientRequest, ClientResponse} from "rickety/client";

import BaseClient from "./client";
import {IGameResult, IGameSubmit, IGameToken, IDeck} from "./types";

class CreateGameClient extends BaseClient {
    async send(request: ClientRequest): Promise<ClientResponse> {
        // Parse and remove body from the request.
        // GET requests cannot have a body.
        const requestBody: {deck: IDeck} = JSON.parse(request.body);
        delete request.body;

        // Add the deck selection as a query parameter in the request url.
        request.url += `?deck=${requestBody.deck}`;

        // Send modified request with parent client.
        const response = await super.send(request);
        const responseBody = JSON.parse(response.body);

        // Extract game token from the response body.
        // JWT logic is hidden from the caller.
        // Original raw token is required to submit the result and is added to the game object.
        const token = responseBody.token;
        const game = jwt.decode(token) as IGameToken;
        game.raw = token;

        // Response body is replaced with modified value before returning.
        response.body = JSON.stringify(game);
        return response;
    }
}

class SubmitGameClient extends BaseClient {
    async send(request: ClientRequest): Promise<ClientResponse> {
        const requestBody: IGameSubmit = JSON.parse(request.body);

        // Request body's token is replaced with the raw string version.
        requestBody.token = requestBody.token.raw as any;
        request.body = JSON.stringify(requestBody);
        return super.send(request);
    }
}

export const CreateGame = new Endpoint<{deck: IDeck}, IGameToken>({
    client: new CreateGameClient(),
    method: "GET",
    path: "/api/game",
});

export const SubmitGame = new Endpoint<IGameSubmit, IGameResult>({
    client: new SubmitGameClient(),
    method: "POST",
    path: "/api/submit",
});
