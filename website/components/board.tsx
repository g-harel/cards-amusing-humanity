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
`;

const Result = styled.div`
    align-content: center;
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    font-size: 3rem;
    font-weight: 600;
    justify-content: center;
    user-select: none;
`;

const Subtitle = styled.div`
    color: #444;
    font-size: 1.6rem;
    height: 4rem;
    text-align: center;
    width: 100%;
`;

const Again = styled.div`
    border-radius: 0.2rem;
    border: 1px solid currentColor;
    color: #444;
    cursor: pointer;
    font-size: 1rem;
    opacity: 0;
    padding: 1rem 2rem;
    text-transform: uppercase;
    transition: opacity 0.4s ease;
`;

const Collapse = styled.div`
    height: 0;
`;

export const Board: React.FunctionComponent = () => {
    const [game, setGame] = useState<IGameToken | null>(null);
    const [selection, setSelection] = useState<ICard | null>(null);
    const [result, setResult] = useState<IGameResult | null>(null);
    const [counting, setCounting] = useState<boolean>(false);

    const submit = (card: ICard) => {
        if (!game) return;
        setSelection(card);
        SubmitGame.call({
            token: game,
            choice: card.id,
        })
            .then(setResult)
            .then(() => setCounting(true));
    };

    const reset = () => {
        setGame(null);
        setSelection(null);
        setResult(null);
        CreateGame.call({extension: "Mini"}).then(setGame);
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
            <Row>
                <Result>
                    <Counter
                        target={result.similarity * 100}
                        callback={() => setCounting(false)}
                    />
                    %<Subtitle>agree</Subtitle>
                    <Again onClick={reset} style={{opacity: counting ? 0 : 1}}>
                        again
                    </Again>
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
                        content={card.text}
                        onClick={() => submit(card)}
                    />
                ))}
            </Row>
        );
    }

    return (
        <Wrapper>
            <Row style={{pointerEvents: "none"}}>
                <Card type="black" content={game.question.text} />
                <div>
                    <Collapse>
                        <Card type="outline" content="" />
                    </Collapse>
                    {selection && (
                        <Card type="white" content={selection.text} />
                    )}
                </div>
            </Row>
            {bottomRowContents}
        </Wrapper>
    );
};
