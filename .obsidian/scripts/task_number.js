module.exports = async (tp) => {
    const filePath = tp.config.configPath + "/scripts/task-id-counter.json";
    const fs = app.vault.adapter;

    let counterData = {};

    // 파일이 존재하면 불러옴
    try {
        const file = await fs.read(filePath);
        counterData = JSON.parse(file);
    } catch (e) {
        counterData = {};
    }

    const today = tp.date.now("YYYYMMDD");
    if (!counterData[today]) {
        counterData[today] = 1;
    } else {
        counterData[today]++;
    }

    await fs.write(filePath, JSON.stringify(counterData));
    return counterData[today].toString().padStart(3, '0');
}
