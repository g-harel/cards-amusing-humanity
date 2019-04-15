import React, {useState, useEffect} from "react";
import styled from "styled-components";

import {CreateGame, SubmitGame} from "../internal/endpoints";
import {IGameToken, IGameResult, ICard, IDeck} from "../internal/types";
import {Button} from "./button";
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

const Selector = styled.div`
    padding: 3rem;
    position: absolute;
    right: 0;
    top: 0;
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

const Collapse = styled.div`
    height: 0;
`;

export const Board: React.FunctionComponent = () => {
    const [game, setGame] = useState<IGameToken | null>(null);
    const [selection, setSelection] = useState<ICard | null>(null);
    const [result, setResult] = useState<IGameResult | null>(null);
    const [counting, setCounting] = useState<boolean>(false);
    const [deck, setDeck] = useState<IDeck>("mini");

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

    const reset = (override?: IDeck) => {
        setGame(null);
        setSelection(null);
        setResult(null);
        CreateGame.call({deck: override || deck}).then(setGame);
    };

    const toggleDeck = () => {
        const decks: IDeck[] = ["mini", "nsfw"];
        const currentIndex = decks.indexOf(deck);
        const nextIndex = (currentIndex + 1) % decks.length;
        setDeck(decks[nextIndex]);
        reset(decks[nextIndex]);
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
                    <Button onClick={reset} hide={counting}>
                        again
                    </Button>
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
            <Selector>
                <Button tight onClick={toggleDeck} color={deck === "nsfw" ? "#bd0a0a" : "green"}>
                    {deck}
                </Button>
            </Selector>
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
