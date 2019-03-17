import React, {useState, useEffect} from "react";
import styled from "styled-components";

import {CreateGame, SubmitGame} from "../internal/endpoints";
import {IGameToken, IGameResult} from "../internal/types";
import {Card} from "./card";

const Wrapper = styled.div`
    display: flex;
    flex-flow: wrap;
    padding: 1rem 1rem 3rem;
    height: 100%;
`;

const Cards = styled.div`
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: center;
`;

const CardRow = styled.div`
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
`;

export const Board: React.FunctionComponent = () => {
    const [game, setGame] = useState<IGameToken | null>(null);
    const [result, setResult] = useState<IGameResult | null>(null);

    useEffect(() => {
        CreateGame.call({}).then(setGame);
    }, []);

    const submit = (id: string) => {
        if (!game) return;
        SubmitGame.call({
            token: game,
            choice: id,
        }).then(setResult);
    };

    return (
        <Wrapper>
            {result && <h1>{result.similarity}</h1>}
            {game && (
                <Cards>
                    <CardRow>
                        <Card
                            type="black"
                            content={game.question.description}
                        />
                        <Card type="outline" content="" />
                    </CardRow>
                    <CardRow>
                        {game.answers.map((ans) => (
                            <Card
                                key={ans.id}
                                type="white"
                                content={ans.description}
                                onClick={() => submit(ans.id)}
                            />
                        ))}
                    </CardRow>
                </Cards>
            )}
        </Wrapper>
    );
};
