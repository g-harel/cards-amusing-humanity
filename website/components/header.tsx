import React from "react";
import styled from "styled-components";

const Wrapper = styled.h1`
    height: 0;
    margin: 0;
    margin: 1em;
    text-shadow: 0 0 4px #121212;
    transform: translate(1rem, 1rem);
    user-select: none;
`;

export const Header: React.FunctionComponent = () => (
    <Wrapper>
        Cards <br /> Amusing <br /> Humanity
    </Wrapper>
);
