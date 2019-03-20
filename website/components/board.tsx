import React, {useState, useEffect} from "react";
import styled from "styled-components";

import {CreateGame, SubmitGame} from "../internal/endpoints";
import {IGameToken, IGameResult, ICard} from "../internal/types";
import {Card} from "./card";
import {Counter} from "./counter";
import {Logo} from "./logo";

const Wrapper = styled.div`
    align-items: center;
    display: flex;
    flex-direction: column;
    min-height: 100%;
    justify-content: center;
    padding: 1rem 1rem 3rem;
`;

const Row = styled.div`
    display: flex;
    flex-wrap: wrap;
    height: 18.8rem;
    justify-content: center;
    transition: opacity 0.4s ease;
`;

const Result = styled.div`
    align-content: center;
    align-items: center;
    font-size: 2rem;
    font-weight: 600;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
`;

const Subtitle = styled.div`
    font-size: 1.2rem;
    text-align: center;
    width: 100%;
`;

const Collapse = styled.div`
    height: 0;
`;

export const Board: React.FunctionComponent = () => {
    const [game, setGame] = useState<IGameToken | null>(null);
    const [selection, setSelection] = useState<ICard | null>(null);
    const [result, setResult] = useState<IGameResult | null>(null);

    const submit = (card: ICard) => {
        if (!game) return;
        setSelection(card);
        SubmitGame.call({
            token: game,
            choice: card.id,
        }).then(setResult);
    };

    const reset = () => {
        setGame(null);
        setSelection(null);
        setResult(null);
        CreateGame.call({}).then((game) => {
            setGame(game);
        });
    };

    // Load a game on initial render.
    useEffect(reset, []);

    if (!game) {
        return (
            <Wrapper>
                <Logo loading scale={0.5} color="#444" />
            </Wrapper>
        );
    }

    let bottomRowContents: React.ReactNode = null;
    if (result) {
        bottomRowContents = (
            <Row onClick={reset}>
                <Result>
                    <Counter target={result.similarity} />%
                    <Subtitle>
                        agree
                    </Subtitle>
                </Result>
            </Row>
        );
    } else if (selection) {
        bottomRowContents = (
            <Row>
                <Result>
                    <Logo loading scale={0.5} color="#444" />
                </Result>
            </Row>
        );
    } else {
        bottomRowContents = (
            <Row>
                {game.answers.map((card) => (
                    <Card
                        key={card.id}
                        type="white"
                        content={card.description}
                        onClick={() => submit(card)}
                    />
                ))}
            </Row>
        );
    }

    return (
        <Wrapper>
            <Row style={{pointerEvents: "none"}}>
                <Card type="black" content={game.question.description} />
                <div>
                    <Collapse>
                        <Card type="outline" content="" />
                    </Collapse>
                    {selection && (
                        <Card type="white" content={selection.description} />
                    )}
                </div>
            </Row>
            {bottomRowContents}
        </Wrapper>
    );
};
