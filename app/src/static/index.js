/**
 * 💡 ES6 (async/await, const, let) 形式で記述
 * Fetch APIでデータを取得し、HTMLテーブルとして表示する
 */
const API_ENDPOINT = "/instruments";
const dataContainer = document.getElementById('data-container');

/**
 * 取得した銘柄リストからHTMLテーブルを生成する関数
 * @param {Array<Object>} instruments - 銘柄情報の配列
 * @returns {string} - 生成されたHTML文字列
 */
const createTableHTML = (instruments) => {
    if (!instruments || instruments.length === 0) {
        return "<p>データが見つかりませんでした。</p>";
    }

    // テーブルヘッダーを定義 (表示順とキー名の定義)
    const headers = {
        ticker: "ティッカー",
        name: "銘柄名",
        instrument_type: "種別",
        exchange: "取引所",
        sector: "業種",
        currency: "通貨",
        country: "国",
    };

    // 1. ヘッダー行の生成
    const headerRow = `<tr>${Object.values(headers).map(header => `<th>${header}</th>`).join('')}</tr>`;

    // 2. データ行の生成
    const dataRows = instruments.map(instrument => {
        // headersで定義された順序でデータセルを生成する
        const cells = Object.keys(headers).map(key => `<td>${instrument[key] || ''}</td>`).join('');
        return `<tr>${cells}</tr>`;
    }).join('');

    return `
        <table>
            <thead>${headerRow}</thead>
            <tbody>${dataRows}</tbody>
        </table>
    `;
};


/**
 * データをフェッチし、コンテナに表示するメイン関数
 */
const loadInstruments = async () => {
    // 既存のローディングメッセージをクリア
    dataContainer.innerHTML = '<p class="loading">データをロード中です...</p>';

    try {
        // 💡 1. Fetch APIの実行
        const response = await fetch(API_ENDPOINT);

        // HTTPステータスが200番台以外の場合、エラーをスロー
        if (!response.ok) {
            throw new Error(`HTTPエラー: ${response.status} ${response.statusText}`);
        }

        // 💡 2. JSONとしてデータを取得
        const instruments = await response.json();
        
        // 💡 3. 取得したデータを基にHTMLを生成し、表示
        const tableHtml = createTableHTML(instruments);
        dataContainer.innerHTML = tableHtml;

    } catch (error) {
        console.error("データ取得中にエラーが発生しました:", error);
        dataContainer.innerHTML = `<p style="color: red;">データ取得失敗: ${error.message}</p>`;
    }
};

// ページロード後に非同期関数を実行
document.addEventListener('DOMContentLoaded', loadInstruments);