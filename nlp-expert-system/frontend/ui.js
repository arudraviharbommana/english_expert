// frontend/ui.js
// UI Controller Module - handles all user interface interactions

class UIController {
  constructor(config = {}) {
    this.backend = config.backend || "http://localhost:8000";
    this.analyzeBtn = document.getElementById('analyzeBtn');
    this.inputSentence = document.getElementById('inputSentence');
    this.origSpan = document.getElementById('orig');
    this.corrSpan = document.getElementById('corr');
    this.imprSpan = document.getElementById('impr');
    this.rulesList = document.getElementById('rulesList');
    this.modeSelect = document.getElementById('mode');
    this.isAnalyzing = false;
    
    this.initEventListeners();
  }
  
  initEventListeners() {
    this.analyzeBtn.addEventListener('click', () => this.analyze());
    this.inputSentence.addEventListener('keydown', (e) => this.handleKeydown(e));
  }
  
  handleKeydown(e) {
    // Analyze on Ctrl+Enter or Cmd+Enter
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      this.analyze();
    }
  }
  
  async analyze() {
    const sentence = this.inputSentence.value.trim();
    if (!sentence) {
      this.showError("Please enter a sentence.");
      return;
    }
    
    if (this.isAnalyzing) return;
    
    this.setAnalyzing(true);
    
    try {
      const response = await fetch(`${this.backend}/process`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sentence: sentence,
          mode: this.modeSelect.value
        })
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      const data = await response.json();
      this.displayResults(data);
      this.triggerAnalysisAnimation();
      
    } catch (error) {
      console.error("Analysis error:", error);
      this.showError(`Error: ${error.message}. Is the backend running on ${this.backend}?`);
    } finally {
      this.setAnalyzing(false);
    }
  }
  
  setAnalyzing(state) {
    this.isAnalyzing = state;
    this.analyzeBtn.disabled = state;
    this.analyzeBtn.textContent = state ? "Analyzing..." : "Analyze & Improve";
  }
  
  displayResults(data) {
    // Display original, corrected, and improved text
    this.origSpan.textContent = data.original || "";
    this.corrSpan.textContent = data.corrected || "";
    this.imprSpan.textContent = data.improved || "";
    
    // Display fired rules
    this.displayRulesList(data.rules_fired);
  }
  
  displayRulesList(rules) {
    this.rulesList.innerHTML = "";
    
    if (!rules || rules.length === 0) {
      const li = document.createElement('li');
      li.textContent = "No rules fired (sentence already clean).";
      li.style.fontStyle = "italic";
      li.style.color = "#999";
      this.rulesList.appendChild(li);
      return;
    }
    
    rules.forEach((rule, index) => {
      const li = document.createElement('li');
      li.className = 'rule-item';
      
      let text = `${index + 1}. ${rule.name}`;
      if (rule.reason) {
        text += `: ${rule.reason}`;
      }
      if (rule.before && rule.after) {
        text += ` — "${rule.before}" → "${rule.after}"`;
      }
      
      li.textContent = text;
      li.title = `Rule: ${rule.name}`;
      this.rulesList.appendChild(li);
    });
  }
  
  showError(message) {
    this.rulesList.innerHTML = "";
    const li = document.createElement('li');
    li.textContent = "⚠️ " + message;
    li.style.color = "#ff6b6b";
    this.rulesList.appendChild(li);
  }
  
  triggerAnalysisAnimation() {
    // Pulse effect on results
    const resultDiv = document.getElementById('results');
    if (resultDiv) {
      resultDiv.classList.add('pulse');
      setTimeout(() => resultDiv.classList.remove('pulse'), 600);
    }
  }
  
  clearResults() {
    this.origSpan.textContent = "";
    this.corrSpan.textContent = "";
    this.imprSpan.textContent = "";
    this.rulesList.innerHTML = "";
  }
  
  setInputText(text) {
    this.inputSentence.value = text;
  }
  
  getInputText() {
    return this.inputSentence.value.trim();
  }
  
  setMode(mode) {
    this.modeSelect.value = mode;
  }
  
  getMode() {
    return this.modeSelect.value;
  }
}

// Export for use in main app
window.UIController = UIController;
