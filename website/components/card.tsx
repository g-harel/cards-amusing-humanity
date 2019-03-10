import React from "react";
import styled, {css} from "styled-components";

interface SharedProps {
    // TODO hover interactions + selected state
    clickable?: boolean;
}

export interface Props extends SharedProps {
    type: "black" | "white" | "outline";
    content: string;
}

interface BaseProps {
    angle?: number;
    x?: number;
    y?: number;
}

const Wrapper = styled.div`
    padding: 3rem;
`;

const Base = styled.div<BaseProps>`
    border-radius: 0.7rem;
    font-weight: 600;
    height: 18rem;
    padding: 1rem 1.5rem;
    width: 13rem;

    /* TODO logo ::after */

    ${(p) => css`
        transform: rotate(${p.angle || 0}deg)
            translate(${p.x || 0}rem, ${p.y || 0}rem);
    `}
`;

const Solid = styled(Base)`
    /* Used to style both "Black" and "White" together */
`;

const Black = styled(Solid)`
    background-color: #000;
    color: #fff;
`;

const White = styled(Solid)`
    background-color: #fff;
    color: #000;
`;

const Shadow = styled(Base)`
    background-color: #000;
    opacity: 0.1;
`;

const Outline = styled(Base)`
    border: 0.1rem dashed #fff;
    opacity: 0.4;
`;

const Collapse = styled.div`
    height: 0;
`;

export const Card: React.StatelessComponent<Props> = (props) => {
    const angle = 10 * (Math.random() - 0.5);

    if (props.type === "outline") {
        return (
            <Wrapper>
                <Outline angle={angle} />
            </Wrapper>
        );
    }

    return (
        <Wrapper>
            <Collapse>
                <Shadow angle={angle} x={-0.8} y={0.5} />
            </Collapse>
            {props.type === "black" ? (
                <Black angle={angle}>{props.content}</Black>
            ) : (
                <White angle={angle}>{props.content}</White>
            )}
        </Wrapper>
    );
};
