function displayCountdown() {
  // const nextRun = new Date();
  const nextRun = new Date(Date.now() + 10000); // 10 detik dari sekarang  
  nextRun.setDate(nextRun.getDate() + 1);
  nextRun.setHours(0, 0, 0, 0);

  const updateCountdown = () => {
    const now = new Date();
    const timeLeft = nextRun - now;
    if (timeLeft <= 0) {
      logger.info('Starting daily transactions...');
      return true;
    }


    const seconds = Math.floor((timeLeft % (1000 * 10)) / 1000);
  
	process.stdout.write(`\rNext run in: ${seconds}s`);
    return false;
  };

  return new Promise((resolve) => {
    const interval = setInterval(() => {
      if (updateCountdown()) {
        clearInterval(interval);
        resolve();
      }
    }, 1000);
  });
}
displayCountdown();
1
1