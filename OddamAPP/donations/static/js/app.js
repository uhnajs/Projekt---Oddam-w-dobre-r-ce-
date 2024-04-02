document.addEventListener("DOMContentLoaded", function() {

  class Help {
    constructor(el) {
      this.el = el;
      this.buttonsContainer = this.el.querySelector(".help--buttons");
      this.slidesContainers = this.el.querySelectorAll(".help--slides");
      this.currentSlide = this.buttonsContainer.querySelector(".active").parentElement.getAttribute('data-id');
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      this.buttonsContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      this.el.addEventListener("click", (e) => {
        if (e.target.classList.contains("btn") && e.target.closest(".help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const btn = e.target;
      this.buttonsContainer.querySelectorAll(".btn").forEach(button => button.classList.remove("active"));
      btn.classList.add("active");
      this.currentSlide = btn.parentElement.getAttribute('data-id');
      this.slidesContainers.forEach(container => {
        container.classList.remove("active");
        if (container.getAttribute('data-id') === this.currentSlide) {
          container.classList.add("active");
        }
      });
    }

    changePage(e) {
      e.preventDefault();
      const page = e.target.getAttribute('data-page');
      // Implement logic to change to the page number received in 'page'
      console.log('Change to page: ', page);
    }
  }

  class FormSelect {
    constructor(el) {
      this.el = el;
      this.options = Array.from(this.el.options);
      this.createDropdown();
      this.bindEvents();
    }

    createDropdown() {
      const dropdown = document.createElement("div");
      dropdown.className = "dropdown";

      this.selected = document.createElement("div");
      this.selected.textContent = this.options[0].text;
      dropdown.appendChild(this.selected);

      this.list = document.createElement("ul");
      this.options.forEach(option => {
        const listItem = document.createElement("li");
        listItem.textContent = option.text;
        listItem.dataset.value = option.value;
        if (option.selected) {
          listItem.classList.add("selected");
          this.selected.textContent = option.text;
        }
        this.list.appendChild(listItem);
      });

      dropdown.appendChild(this.list);
      this.el.style.display = 'none';
      this.el.parentNode.insertBefore(dropdown, this.el.nextSibling);
    }

    bindEvents() {
      this.selected.addEventListener("click", () => {
        this.list.classList.toggle("show");
      });

      this.list.querySelectorAll("li").forEach(listItem => {
        listItem.addEventListener("click", (e) => {
          this.selected.textContent = e.target.textContent;
          this.list.querySelector(".selected")?.classList.remove("selected");
          e.target.classList.add("selected");
          this.el.value = e.target.dataset.value;
          this.list.classList.remove("show");
        });
      });
    }
  }

  class FormSteps {
    constructor(form) {
      this.form = form;
      this.nextButtons = this.form.querySelectorAll(".next-step");
      this.prevButtons = this.form.querySelectorAll(".prev-step");
      this.stepsCounter = this.form.querySelector(".form--steps-counter span");
      this.currentStep = 1;
      this.stepsForms = this.form.querySelectorAll("form > div");
      this.donationData = {};
      this.bindEvents();
    }

    bindEvents() {
      this.nextButtons.forEach(button => {
        button.addEventListener("click", e => {
          e.preventDefault();
          this.collectData(this.currentStep);
          if (this.validateCurrentStep()) {
            this.goToNextStep();
          }
        });
      });

      this.prevButtons.forEach(button => {
        button.addEventListener("click", e => {
          e.preventDefault();
          this.goToPrevStep();
        });
      });

      this.form.addEventListener("submit", e => {
        e.preventDefault();
        this.submitForm();
      });
    }

    collectData(step) {
      // Logic to collect data based on step
      // Update this.donationData with the values from the form elements
    }

    validateCurrentStep() {
      // Logic to validate current step fields
      // Return true if valid, false otherwise
      return true;
    }
    goToNextStep() {
      this.currentStep++;
      if (this.currentStep > 5) this.currentStep = 5; // Zapobiegaj przekroczeniu liczby kroków
      this.updateStepDisplay();
    }

    goToPrevStep() {
      this.currentStep--;
      if (this.currentStep < 1) this.currentStep = 1; // Zapobiegaj spadaniu poniżej 1
      this.updateStepDisplay();
    }

    updateStepDisplay() {
      this.stepsCounter.textContent = this.currentStep;
      this.stepsForms.forEach(form => {
        form.classList.remove("active");
        if (parseInt(form.dataset.step, 10) === this.currentStep) {
          form.classList.add("active");
        }
      });
    }
    submitForm() {
      // AJAX request to submit the form data
      // Use this.donationData as the data to submit
    }
  }

  // Initialization code
  const helpSectionElement = document.querySelector(".help");
  if (helpSectionElement) {
    new Help(helpSectionElement);
  }

  document.querySelectorAll(".form-group--dropdown select").forEach(selectElement => {
    new FormSelect(selectElement);
  });

  const formStepsElement = document.querySelector(".form--steps");
  if (formStepsElement) {
    new FormSteps(formStepsElement);
  }
});
