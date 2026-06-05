/** Normalise un prix saisi (espaces, virgule décimale) et limite à 10 chiffres entiers. */
export function parsePriceInput(value: string | number): string {
  if (typeof value === 'number') return String(value)

  const cleaned = value
    .replace(/\s/g, '')
    .replace(',', '.')
    .replace(/[^\d.]/g, '')

  if (!cleaned) return '0'

  const [integerPart, ...rest] = cleaned.split('.')
  const decimals = rest.join('').slice(0, 2)
  const digits = integerPart.replace(/^0+(?=\d)/, '') || '0'

  if (digits.length > 10) {
    throw new Error('Le prix ne peut pas dépasser 10 chiffres.')
  }

  return decimals ? `${digits}.${decimals}` : digits
}

export function countPriceDigits(value: string | number): number {
  const parsed = parsePriceInput(String(value))
  return parsed.split('.')[0].replace(/\D/g, '').length
}
