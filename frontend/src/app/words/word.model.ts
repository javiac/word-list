export class Word {
    constructor(
        public value: string,
        public order: number,
        public id?: number,
        public updatedAt?: Date,
        public createdAt?: Date,
    ) { }
}
