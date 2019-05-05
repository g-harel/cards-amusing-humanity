import jwt from "jsonwebtoken";
import {DefaultClient} from "rickety";
import {ClientRequest, ClientResponse} from "rickety/client";

import {IGameToken} from "./types";

// Mock requests when hosted on "GitHub Pages".
class MockClient extends DefaultClient {
    async send(request: ClientRequest): Promise<ClientResponse> {
        if (!window.location.hostname.endsWith("github.io")) {
            return super.send(request);
        }

        if (request.url.startsWith("/api/game")) {
            const mockGame: IGameToken = {
                raw: "",
                question: {
                    id: "",
                    text: "What gets better with age?",
                    deck: "",
                },
                answers: [
                    {id: "1", text: "Daddy's credit card.", deck: ""},
                    {id: "2", text: "Drinking alone.", deck: ""},
                    {id: "3", text: "The glass ceiling.", deck: ""},
                    {id: "4", text: "A lifetime of sadness.", deck: ""},
                    {id: "5", text: "A PowerPoint presentation.", deck: ""},
                ],
            };
            const token = jwt.sign(mockGame, "-");
            return {status: 200, body: JSON.stringify({token})};
        }

        if (request.url.startsWith("/api/submit")) {
            return {
                status: 200,
                body: JSON.stringify({
                    similarity: 0.9 * Math.random(),
                }),
            };
        }

        return {status: 501, body: "Not Implemented"};
    }
}

// Delay all requests to simulate network latency.
class DelayClient extends MockClient {
    async send(request: ClientRequest): Promise<ClientResponse> {
        await new Promise((res) => setTimeout(res, 400 + 200 * Math.random()));
        return super.send(request);
    }
}

export default DelayClient;
