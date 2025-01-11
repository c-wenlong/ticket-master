type HttpResponse<T = any> = {
  base: {
    code: number;
    message: string;
    errorMessage?: string;
  };
  data?: T;
};
