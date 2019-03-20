import React from "react";
import styled, {css} from "styled-components";

export interface IProps {
    type: "black" | "white" | "outline";
    content: string;
    onClick?: () => any;
}

interface IBaseProps {
    angle?: number;
    x?: number;
    y?: number;
}

// CSS helper to generate the translate transform.
const translate = (x?: number, y?: number) => {
    return `translate(${x || 0}rem, ${y || 0}rem)`;
};

// CSS helper to generate the rotate transform.
const rotate = (angle?: number, offset?: number) => {
    angle = angle || 0;

    if (offset) {
        if (angle < 0) {
            angle += offset;
        } else {
            angle -= offset;
        }
    }

    return `rotate(${angle}deg)`;
};

const Wrapper = styled.div`
    padding: 1.4rem;
`;

const Base = styled.div<IBaseProps>`
    border-radius: 0.6rem;
    font-size: 0.9rem;
    font-weight: 600;
    height: 16rem;
    padding: 0.9rem 1.3rem;
    transition: transform 0.1s ease;
    user-select: none;
    width: 12rem;

    /* TODO logo ::after */

    ${({x, y, angle}) => css`
        transform: ${rotate(angle)} ${translate(x, y)};
    `}
`;

// Parent of both "Black" and "White" together.
const Solid = styled(Base)<IBaseProps>`
    cursor: pointer;

    &:hover {
        ${({x, y, angle}) => css`
            transform: scale(1.01) ${rotate(angle, 0.5)}
                ${translate(x, (y || 0) - 0.2)};
        `}
    }

    &:active {
        /* Remove hover state's scale transform. */
        ${({x, y, angle}) => css`
            transform: ${rotate(angle, 0.5)} ${translate(x, y)};
        `}
    }
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
    opacity: 0.2;
`;

const Outline = styled(Base)`
    border: 0.1rem dashed #fff;
    opacity: 0.4;
    transform: scale(1.02) rotate(0);
`;

const Collapse = styled.div`
    height: 0;
`;

export const Card: React.FunctionComponent<IProps> = (props) => {
    // Deterministic angle calculation using first two chars from content.
    // Randomness would cause the angle to change on each render.
    const content = (props.content || "").padEnd(2, " ");
    const angle = ((content.charCodeAt(0) + content.charCodeAt(1)) % 11) - 5;

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
                <Black angle={angle} onClick={props.onClick}>
                    {props.content}
                </Black>
            ) : (
                <White angle={angle} onClick={props.onClick}>
                    {props.content}
                </White>
            )}
        </Wrapper>
    );
};
