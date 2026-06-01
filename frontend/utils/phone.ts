/** BE, FR, LU, NL — national (0…) ou international (+32, +33, +352, +31) */
export const PHONE_REGEX =
  /^(?:\+32[\s./-]?(?:\d[\s./-]?){8,12}|0032[\s./-]?(?:\d[\s./-]?){8,12}|\+33[\s./-]?(?:\d[\s./-]?){8,11}|0033[\s./-]?(?:\d[\s./-]?){8,11}|\+352[\s./-]?(?:\d[\s./-]?){6,11}|00352[\s./-]?(?:\d[\s./-]?){6,11}|\+31[\s./-]?(?:\d[\s./-]?){8,11}|0031[\s./-]?(?:\d[\s./-]?){8,11}|0[\s./-]?(?:\d[\s./-]?){8,11}|[26]\d[\s./-]?(?:\d[\s./-]?){6,9})$/

export function isValidPhone(value: string): boolean {
  const trimmed = value.trim()
  return trimmed === '' || PHONE_REGEX.test(trimmed)
}
