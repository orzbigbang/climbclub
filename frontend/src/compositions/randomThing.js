const getRandomNumbers = (min, max, count) => {
  const range = Array.from({ length: max - min + 1 }, (_, i) => i + min);

  for (let i = range.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [range[i], range[j]] = [range[j], range[i]];
  }

  return range.slice(0, count);
}

const colors = [
  "#FAF3DD",
  "#6fdc73",
  "#FFEB3B",
  "#FF9800",
  "#97b7f8",
]

const sentences = [
  "Mountains are not fair or unfair, they are just dangerous.",
  "Mountains are not stadiums where I satisfy my ambition to achieve; they are the cathedrals where I practice my religion.",
  "Climb the mountain not to plant your flag, but to embrace the challenge, enjoy the air, and behold the view.",
  "The best climber in the world is the one having the most fun.",
  "Getting to the top is optional. Getting down is mandatory.",
  "Climbing is not about conquering the mountain; it's about conquering yourself.",
  "The summit is not the end; it's the beginning.",
  "Every mountain top is within reach if you just keep climbing.",
  "The climb might be tough and challenging, but the view is worth it.",
  "The mountains are calling, and I must go.",
  "It is not the mountain we conquer but ourselves.",
  "In the mountains, there are only two grades: You can either do it, or you can't.",
  "The mountains have rules. They are harsh rules, but they are there, and if you keep to them, you are safe.",
  "When you go to the mountains, you see them and you admire them. In a sense, they give you a challenge, and you try to express that challenge by climbing them.",
  "The mountains are a demanding, cold place, and they don't allow for mistakes.",
  "The mountains are the last place where man can feel truly wild.",
  "The mountains are the means; the man is the end. The goal is not to reach the tops of mountains, but to improve the man.",
  "The mountains are a mirror, reflecting the changes in your life.",
  "The mountains are a refuge from the world below.",
  "The mountains are a reminder that the world is still wild and full of wonders."
]

export const getRandomSentences = (count=5) => {
  const randomNumbers = getRandomNumbers(0, sentences.length - 1, count)
  const randomSentences = []
  
  for (let num of randomNumbers) {
    randomSentences.push(sentences[num])
  }

  return randomSentences
}


export const getRandomColors = (count=5) => {
  return colors
}

