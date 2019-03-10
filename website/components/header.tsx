import React from "react";
import styled from "styled-components";

const Wrapper = styled.h1`
    margin: 1em 0 0 1em;
    text-shadow: 0 0 4px #121212;
    user-select: none;
`;

export const Header: React.StatelessComponent = () => (
    <Wrapper>
        Cards
        <br />
        Against
        <br />
        Humanity
    </Wrapper>
);
