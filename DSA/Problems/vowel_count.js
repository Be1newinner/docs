const str = 'my name is vijay kumar. I am from delhi.';

console.time("Optimized For Loop");

// Define vowel and consonant sets
const vowels = new Set("aeiou");
const consonants = new Set("bcdfghjklmnpqrstvwxyz");

// Initialize counters
const vowelCounts = { a: 0, e: 0, i: 0, o: 0, u: 0 };
let totalVowels = 0, totalConsonants = 0;

for (let i = 0; i < str.length; i++) {
    const char = str[i].toLowerCase();
    
    if (vowels.has(char)) {
        vowelCounts[char]++;
        totalVowels++;
    } else if (consonants.has(char)) {
        totalConsonants++;
    }

}

console.log({ vowels: totalVowels, consonants: totalConsonants }, vowelCounts);

console.timeEnd("Optimized For Loop");







