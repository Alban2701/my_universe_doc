
import slugify from "slugify";

export const toSlug = (text: string) => {
    return slugify(text, {
        lower: true,
        strict: true,
        remove: /[*+~.()'"!:@]/g,
    });
};