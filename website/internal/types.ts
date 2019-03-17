export interface ICard {
    id: string;
    description: string;
}

export interface IGameToken {
    question: ICard;
    answers: ICard[];
    raw: string;
}

export interface IGameSubmit {
    token: IGameToken;
    choice: string;
}

export interface IGameResult {
    similarity: number;
}
