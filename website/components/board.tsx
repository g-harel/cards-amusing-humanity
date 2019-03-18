import React, {useState, useEffect} from "react";
import styled from "styled-components";

import {CreateGame, SubmitGame} from "../internal/endpoints";
import {IGameToken, IGameResult, ICard} from "../internal/types";
import {Card} from "./card";

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
    justify-content: center;
    transition: opacity 0.4s ease;
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
        return <Wrapper>loading</Wrapper>;
    }

    let bottomRowContents: React.ReactNode = null;
    if (result) {
        bottomRowContents = <Row onClick={reset}>{result.similarity}</Row>;
    } else if (selection) {
        bottomRowContents = <Row>loading</Row>;
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
