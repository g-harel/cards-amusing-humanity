export type Extension = "Base" | "Mini";

export interface ICard {
    id: string;
    text: string;
    extension: string;
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
