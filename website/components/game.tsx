import React from "react";
import styled from "styled-components";

import {ICard} from "../internal/types";
import {Card} from "./card";
import {Title} from "./title";

export interface Props {
    black: ICard;
    white: [ICard, ICard, ICard, ICard, ICard];
    onPick: (id: string) => any;
}

const Wrapper = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
`;

const Row = styled.div`
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
`;

const Stretch = styled.div`
    flex-grow: 1;
    flex-shrink: 1;
`;

export const Game: React.FunctionComponent<Props> = (props) => (
    <Wrapper>
        <Row>
            <Title />
            <Stretch />
            <Card type="black" content={props.black.description} />
            <Card type="outline" content="" />
            <Stretch />
        </Row>
        <Row>
            {props.white.map((c) => (
                <Card
                    key={c.id}
                    type="white"
                    content={c.description}
                    onClick={() => props.onPick(c.id)}
                />
            ))}
        </Row>
    </Wrapper>
);
