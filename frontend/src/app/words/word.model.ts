export interface IWord{
    value: string;
    order: number;
    _id?: {'$oid': string};
    updatedAt?: Date;
    createdAt?: Date;
}

export class Word {
    constructor(
        public value: string,
        public order: number,
        public _id?: {'$oid': string},
        public updatedAt?: Date,
        public createdAt?: Date,
    ) { }
}
